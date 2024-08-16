import json
import loguru
import math
import os
import random
import sys
import time
from dataclasses import asdict, dataclass
from enum import Enum
from itertools import chain
from typing import Any, Callable, Dict, Tuple

import datasets
import evaluate
import jax
import jax.numpy as jnp
import numpy as np
import optax
from optax import Schedule
from datasets.load import DatasetDict
from datasets import ClassLabel, load_dataset
from flax import struct, traverse_util
from flax.jax_utils import pad_shard_unpad, replicate, unreplicate
from flax.training import train_state
from flax.training.common_utils import get_metrics, onehot, shard
from tqdm import tqdm

import transformers
from transformers import (
    AutoConfig,
    AutoTokenizer,
    FlaxAutoModelForTokenClassification,
    HfArgumentParser,
    is_tensorboard_available,
)

from materials_spum_multi.util import NumpyEncoder


Array = Any
Dataset = datasets.arrow_dataset.Dataset
PRNGKey = Any


@dataclass
class TrainingArguments:
    output_dir: str
    overwrite_output_dir: bool = False
    do_train: bool = False
    do_eval: bool = False
    per_device_train_batch_size: int = 8
    per_device_eval_batch_size: int = 8
    learning_rate: float = 5e-5
    weight_decay: float = 0.0
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    adam_epsilon: float = 1e-8
    adafactor: bool = False
    num_train_epochs: float = 3.0
    warmup_steps: int = 0
    logging_steps: int = 500
    save_steps: int = 500
    eval_steps: int | None = None
    seed: int = 42
    is_split_into_words: bool = False

    def __post_init__(self):
        if self.output_dir is not None:
            self.output_dir = os.path.expanduser(self.output_dir)

    def to_dict(self):
        d = asdict(self)
        for k, v in d.items():
            if isinstance(v, Enum):
                d[k] = v.value
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], Enum):
                d[k] = [x.value for x in v]
            if k.endswith("_token"):
                d[k] = f"<{k.upper()}>"
        return d


@dataclass
class ModelArguments:
    model_name_or_path: str
    config_name: str | None = None
    tokenizer_name: str | None = None
    cache_dir: str | None = None
    model_revision: str = "main"


@dataclass
class DataTrainingArguments:
    task_name: str = "ner"
    dataset_name: str | None = None
    dataset_config_name: str | None = None
    train_file: str | None = None
    validation_file: str | None = None
    test_file: str | None = None
    text_column_name: str | None = None
    label_column_name: str | None = None
    overwrite_cache: bool = False
    preprocessing_num_workers: int | None = None
    max_seq_length: int | None = None
    max_train_samples: int | None = None
    max_eval_samples: int | None = None
    max_predict_samples: int | None = None
    label_all_tokens: bool = False
    return_entity_level_metrics: bool = False

    def __post_init__(self):
        if (
            self.dataset_name is None
            and self.train_file is None
            and self.validation_file is None
        ):
            raise ValueError(
                "Need either a dataset name or a training/validation file."
            )
        else:
            if self.train_file is not None:
                extension = self.train_file.split(".")[-1]
                assert extension in [
                    "csv",
                    "json",
                ], "`train_file` should be a csv or a json file."
            if self.validation_file is not None:
                extension = self.validation_file.split(".")[-1]
                assert extension in [
                    "csv",
                    "json",
                ], "`validation_file` should be a csv or a json file."
        self.task_name = self.task_name.lower()


def create_train_state(
    model: FlaxAutoModelForTokenClassification,
    learning_rate_fn: Schedule,
    num_labels: int,
    training_args: TrainingArguments,
) -> train_state.TrainState:
    """Create initial training state."""

    class TrainState(train_state.TrainState):
        """Train state with an Optax optimizer.

        The two functions below differ depending on whether the task is classification
        or regression.

        Args:
          logits_fn: Applied to last layer to obtain the logits.
          loss_fn: Function to compute the loss.
        """

        logits_fn: Callable = struct.field(pytree_node=False)
        loss_fn: Callable = struct.field(pytree_node=False)

    # We use Optax's "masking" functionality to not apply weight decay
    # to bias and LayerNorm scale parameters. decay_mask_fn returns a
    # mask boolean with the same structure as the parameters.
    # The mask is True for parameters that should be decayed.
    def decay_mask_fn(params):
        flat_params = traverse_util.flatten_dict(params)
        # find out all LayerNorm parameters
        layer_norm_candidates = ["layernorm", "layer_norm", "ln"]
        layer_norm_named_params = {
            layer[-2:]
            for layer_norm_name in layer_norm_candidates
            for layer in flat_params.keys()
            if layer_norm_name in "".join(layer).lower()
        }
        flat_mask = {
            path: (path[-1] != "bias" and path[-2:] not in layer_norm_named_params)
            for path in flat_params
        }
        return traverse_util.unflatten_dict(flat_mask)

    tx = optax.adamw(
        learning_rate=learning_rate_fn,
        b1=training_args.adam_beta1,
        b2=training_args.adam_beta2,
        eps=training_args.adam_epsilon,
        weight_decay=training_args.weight_decay,
        mask=decay_mask_fn,
    )

    def cross_entropy_loss(logits, labels):
        xentropy = optax.softmax_cross_entropy(
            logits, onehot(labels, num_classes=num_labels)
        )
        return jnp.mean(xentropy)

    return TrainState.create(
        apply_fn=model.__call__,  # type: ignore
        params=model.params,  # type: ignore
        tx=tx,
        logits_fn=lambda logits: logits.argmax(-1),
        loss_fn=cross_entropy_loss,
    )


def create_learning_rate_fn(
    train_ds_size: int,
    train_batch_size: int,
    num_train_epochs: int,
    num_warmup_steps: int,
    learning_rate: float,
) -> Schedule:
    """Returns a linear warmup, linear_decay learning rate function."""
    steps_per_epoch = train_ds_size // train_batch_size
    num_train_steps = steps_per_epoch * num_train_epochs
    warmup_fn = optax.linear_schedule(
        init_value=0.0, end_value=learning_rate, transition_steps=num_warmup_steps
    )
    decay_fn = optax.linear_schedule(
        init_value=learning_rate,
        end_value=0,
        transition_steps=num_train_steps - num_warmup_steps,
    )
    schedule_fn = optax.join_schedules(
        schedules=[warmup_fn, decay_fn], boundaries=[num_warmup_steps]
    )
    return schedule_fn


def train_data_collator(rng: PRNGKey, dataset: Dataset, batch_size: int):
    """Returns shuffled batches of size `batch_size` from truncated `train dataset`, sharded over all local devices."""
    steps_per_epoch = len(dataset) // batch_size
    perms = jax.random.permutation(rng, len(dataset))
    perms = perms[: steps_per_epoch * batch_size]  # Skip incomplete batch.
    perms = perms.reshape((steps_per_epoch, batch_size))

    for perm in perms:
        batch = dataset[perm]
        batch = {k: np.array(v) for k, v in batch.items()}
        batch = shard(batch)

        yield batch


def eval_data_collator(dataset: Dataset, batch_size: int):
    """Returns batches of size `batch_size` from `eval dataset`. Sharding handled by `pad_shard_unpad` in the eval loop."""
    batch_idx = np.arange(len(dataset))

    steps_per_epoch = math.ceil(len(dataset) / batch_size)
    batch_idx = np.array_split(batch_idx, steps_per_epoch)

    for idx in batch_idx:
        batch = dataset[idx]
        batch = {k: np.array(v) for k, v in batch.items()}

        yield batch


def main():
    # parsing arguments
    parser = HfArgumentParser(
        (ModelArguments, DataTrainingArguments, TrainingArguments)  # type: ignore
    )
    model_args, data_args, training_args = parser.parse_args_into_dataclasses()

    # setting up logging
    log_level = "INFO" if jax.process_index() == 0 else "ERROR"
    logger = loguru.logger.bind(name="__name__")
    logger.remove()
    logger.add(sys.stderr, level=log_level)
    if jax.process_index() == 0:
        datasets.utils.logging.set_verbosity_warning()
        transformers.utils.logging.set_verbosity_info()
    else:
        datasets.utils.logging.set_verbosity_error()
        transformers.utils.logging.set_verbosity_error()

    # loading dataset
    data_files = {}
    if data_args.train_file is not None:
        data_files["train"] = data_args.train_file
    if data_args.validation_file is not None:
        data_files["validation"] = data_args.validation_file
    if data_args.test_file is not None:
        data_files["test"] = data_args.test_file
    extension = (
        data_args.train_file
        if data_args.train_file is not None
        else data_args.valid_file
    ).split(".")[-1]
    raw_datasets: DatasetDict = load_dataset(
        extension,
        data_files=data_files,
        cache_dir=model_args.cache_dir,
    )  # type: ignore

    if raw_datasets["train"] is not None:
        column_names = raw_datasets["train"].column_names
        features = raw_datasets["train"].features
    else:
        column_names = raw_datasets["validation"].column_names
        features = raw_datasets["validation"].features

    # converting features
    if data_args.text_column_name is not None:
        text_column_name = data_args.text_column_name
    elif "tokens" in column_names:
        text_column_name = "tokens"
    else:
        text_column_name = column_names[0]

    if data_args.label_column_name is not None:
        label_column_name = data_args.label_column_name
    elif f"{data_args.task_name}_tags" in column_names:
        label_column_name = f"{data_args.task_name}_tags"
    else:
        label_column_name = column_names[1]

    def get_label_list(labels):
        unique_labels = set()
        for label in labels:
            unique_labels = unique_labels | set(label)
        label_list = list(unique_labels)
        label_list.sort()
        return label_list

    if isinstance(features[label_column_name].feature, ClassLabel):
        label_list = features[label_column_name].feature.names
        # No need to convert the labels since they are already ints.
        label_to_id = {i: i for i in range(len(label_list))}
    else:
        label_list = get_label_list(raw_datasets["train"][label_column_name])
        label_to_id = {label: i for i, label in enumerate(label_list)}
    num_labels = len(label_list)

    # loading model and tokenizer
    config = AutoConfig.from_pretrained(
        model_args.config_name
        if model_args.config_name
        else model_args.model_name_or_path,
        num_labels=num_labels,
        label2id=label_to_id,
        id2label={i: label for label, i in label_to_id.items()},
        finetuning_task=data_args.task_name,
        cache_dir=model_args.cache_dir,
        revision=model_args.model_revision,
    )
    tokenizer_name_or_path = (
        model_args.tokenizer_name
        if model_args.tokenizer_name
        else model_args.model_name_or_path
    )
    if config.model_type in {"gpt2", "roberta"}:
        tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name_or_path,
            cache_dir=model_args.cache_dir,
            revision=model_args.model_revision,
            add_prefix_space=True,
        )
    else:
        tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name_or_path,
            cache_dir=model_args.cache_dir,
            revision=model_args.model_revision,
        )
    model = FlaxAutoModelForTokenClassification.from_pretrained(
        model_args.model_name_or_path,
        config=config,
        cache_dir=model_args.cache_dir,
        revision=model_args.model_revision,
    )

    # Preprocessing the datasets
    # Tokenize all texts and align the labels with them.
    def tokenize_and_align_labels(examples):
        tokenized_inputs = tokenizer(
            examples[text_column_name],
            max_length=data_args.max_seq_length,
            padding="max_length",
            truncation=True,
            is_split_into_words=False,
        )

        labels = []

        for i, label in enumerate(examples[label_column_name]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                # Special tokens have a word id that is None. We set the label to -100 so they are automatically
                # ignored in the loss function.
                if word_idx is None:
                    label_ids.append(-100)
                # We set the label for the first token of each word.
                elif word_idx != previous_word_idx:
                    label_ids.append(label_to_id[label[word_idx]])
                # For the other tokens in a word, we set the label to either the current label or -100, depending on
                # the label_all_tokens flag.
                else:
                    label_ids.append(
                        label_to_id[label[word_idx]]
                        if data_args.label_all_tokens
                        else -100
                    )
                previous_word_idx = word_idx

            labels.append(label_ids)
        tokenized_inputs["labels"] = labels
        return tokenized_inputs

    def tokenize_and_align_labels_char(examples):
        tokenized_inputs = tokenizer(
            examples[text_column_name],
            max_length=data_args.max_seq_length,
            padding="max_length",
            truncation=True,
            # We use this argument because the texts in our dataset are lists of words (with a label for each word).
            is_split_into_words=True,
        )
        # input: ['1', '.', '如', '上', '钢', ...]
        labels = []
        for i, label in enumerate(examples[label_column_name]):
            word_ids = tokenized_inputs.word_ids(batch_index=i)
            previous_word_idx = None
            label_ids = []
            for word_idx in word_ids:
                # Special tokens have a word id that is None.
                # We set the label to -100 so they are automatically
                # ignored in the loss function.
                if word_idx is None:
                    label_ids.append(-100)
                # We set the label for the first token of each word.
                elif word_idx != previous_word_idx:
                    label_ids.append(label_to_id[label[word_idx]])
                # For the other tokens in a word, we set the label to
                # either the current label or -100, depending on
                # the label_all_tokens flag.
                else:
                    label_ids.append(
                        label_to_id[label[word_idx]]
                        if data_args.label_all_tokens
                        else -100
                    )
                previous_word_idx = word_idx

            labels.append(label_ids)
        tokenized_inputs["labels"] = labels
        return tokenized_inputs

    token_and_algin_fn = (
        tokenize_and_align_labels_char
        if training_args.is_split_into_words
        else tokenize_and_align_labels
    )
    processed_raw_datasets = raw_datasets.map(
        token_and_algin_fn,
        batched=True,
        num_proc=data_args.preprocessing_num_workers,
        load_from_cache_file=not data_args.overwrite_cache,
        remove_columns=raw_datasets["train"].column_names,
        desc="Running tokenizer on dataset",
    )

    train_dataset = processed_raw_datasets["train"]
    eval_dataset = processed_raw_datasets["validation"]
    test_dataset = processed_raw_datasets["test"]

    # Log a few random samples from the training set:
    for index in random.sample(range(len(train_dataset)), 1):
        logger.info(f"Sample {index} of the training set: {train_dataset[index]}.")

    # Define a summary writer
    has_tensorboard = is_tensorboard_available()
    logger.info(f"Tensorboard is {'available' if has_tensorboard else 'unavailable'}")
    if has_tensorboard and jax.process_index() == 0:
        try:
            from torch.utils.tensorboard import SummaryWriter   # type: ignore

            summary_writer = SummaryWriter(training_args.output_dir)
            summary_writer.add_hparams(
                {**training_args.to_dict(), **vars(model_args), **vars(data_args)}, {}
            )
        except ImportError as ie:
            has_tensorboard = False
            logger.warning(
                f"Unable to display metrics through TensorBoard because some package are not installed: {ie}"
            )
    else:
        logger.warning(
            "Unable to display metrics through TensorBoard because the package is not installed: "
            "Please run pip install tensorboard to enable."
        )

    def write_train_metric(summary_writer, train_metrics, train_time, step):
        summary_writer.add_scalar("train_time", train_time, step)

        train_metrics = get_metrics(train_metrics)
        for key, vals in train_metrics.items():
            tag = f"train_{key}"
            for i, val in enumerate(vals):
                summary_writer.add_scalar(tag, val, step - len(vals) + i + 1)

    def write_eval_metric(summary_writer, eval_metrics, step):
        for metric_name, value in eval_metrics.items():
            summary_writer.add_scalar(f"eval_{metric_name}", value, step)

    num_epochs = int(training_args.num_train_epochs)
    logger.info(f"Training on {num_epochs} epochs")
    rng = jax.random.PRNGKey(training_args.seed)
    dropout_rngs = jax.random.split(rng, jax.local_device_count())

    train_batch_size = (
        training_args.per_device_train_batch_size * jax.local_device_count()
    )
    per_device_eval_batch_size = int(training_args.per_device_eval_batch_size)
    eval_batch_size = (
        training_args.per_device_eval_batch_size * jax.local_device_count()
    )
    logger.info(f"Train batch size: {train_batch_size}, Eval batch size: {eval_batch_size}")

    learning_rate_fn = create_learning_rate_fn(
        len(train_dataset),
        train_batch_size,
        training_args.num_train_epochs,
        training_args.warmup_steps,
        training_args.learning_rate,
    )

    state = create_train_state(
        model, learning_rate_fn, num_labels=num_labels, training_args=training_args
    )

    # define step functions
    def train_step(
        state: train_state.TrainState, batch: Dict[str, Array], dropout_rng: PRNGKey
    ) -> Tuple[train_state.TrainState, float, float]:
        """Trains model with an optimizer (both in `state`) on `batch`, returning a pair `(new_state, loss)`."""
        dropout_rng, new_dropout_rng = jax.random.split(dropout_rng)
        targets = batch.pop("labels")

        def loss_fn(params):
            logits = state.apply_fn(
                **batch, params=params, dropout_rng=dropout_rng, train=True
            )[0]
            loss = state.loss_fn(logits, targets)  # type: ignore
            return loss

        grad_fn = jax.value_and_grad(loss_fn)
        loss, grad = grad_fn(state.params)
        grad = jax.lax.pmean(grad, "batch")
        new_state = state.apply_gradients(grads=grad)
        metrics = jax.lax.pmean(
            {"loss": loss, "learning_rate": learning_rate_fn(state.step)},
            axis_name="batch",
        )
        return new_state, metrics, new_dropout_rng

    p_train_step = jax.pmap(train_step, axis_name="batch", donate_argnums=(0,))
    logger.info("Train step compiled")

    def eval_step(state, batch):
        logits = state.apply_fn(**batch, params=state.params, train=False)[0]
        return state.logits_fn(logits)

    p_eval_step = jax.pmap(eval_step, axis_name="batch")
    logger.info("Eval step compiled")

    metric = evaluate.load("seqeval", cache_dir=model_args.cache_dir)
    logger.info("Seqeval metric loaded")

    def get_labels(y_pred, y_true):
        # Transform predictions and references tensos to numpy arrays

        # Remove ignored index (special tokens)
        true_predictions = [
            [label_list[p] for (p, label) in zip(pred, gold_label) if label != -100]
            for pred, gold_label in zip(y_pred, y_true)
        ]
        true_labels = [
            [label_list[label] for (p, label) in zip(pred, gold_label) if label != -100]
            for pred, gold_label in zip(y_pred, y_true)
        ]
        return true_predictions, true_labels

    def compute_metrics():
        results = metric.compute() or {}
        if data_args.return_entity_level_metrics:
            # Unpack nested dictionaries
            final_results = {}
            for key, value in results.items():
                if isinstance(value, dict):
                    for n, v in value.items():
                        final_results[f"{key}_{n}"] = v
                else:
                    final_results[key] = value
            return final_results
        else:
            return {
                "precision": results["overall_precision"],
                "recall": results["overall_recall"],
                "f1": results["overall_f1"],
                "accuracy": results["overall_accuracy"],
            }

    logger.info(f"===== Starting training ({num_epochs} epochs) =====")
    train_time = 0

    # make sure weights are replicated on each device
    state = replicate(state)

    train_time = 0
    step_per_epoch = len(train_dataset) // train_batch_size
    total_steps = step_per_epoch * num_epochs
    epochs = tqdm(range(num_epochs), desc=f"Epoch ... (1/{num_epochs})", position=0)
    for epoch in epochs:
        train_start = time.time()
        train_metrics = []

        # Create sampling rng
        rng, input_rng = jax.random.split(rng)

        # train
        for step, batch in enumerate(
            tqdm(
                train_data_collator(input_rng, train_dataset, train_batch_size),
                total=step_per_epoch,
                desc="Training...",
                position=1,
            )
        ):
            state, train_metric, dropout_rngs = p_train_step(state, batch, dropout_rngs)
            train_metrics.append(train_metric)

            cur_step = (epoch * step_per_epoch) + (step + 1)

            if cur_step % training_args.logging_steps == 0 and cur_step > 0:
                # Save metrics
                train_metric = unreplicate(train_metric)
                train_time += time.time() - train_start
                if has_tensorboard and jax.process_index() == 0:
                    write_train_metric(
                        summary_writer,
                        train_metrics,
                        train_time,
                        cur_step,  # type: ignore
                    )

                epochs.write(
                    f"Step... ({cur_step}/{total_steps} | Training Loss: {train_metric['loss']}, Learning Rate:"
                    f" {train_metric['learning_rate']})"
                )

                train_metrics = []

            if cur_step % training_args.eval_steps == 0 and cur_step > 0:
                eval_metrics = {}
                # evaluate
                for batch in tqdm(
                    eval_data_collator(eval_dataset, eval_batch_size),
                    total=math.ceil(len(eval_dataset) / eval_batch_size),
                    desc="Evaluating ...",
                    position=2,
                ):
                    labels = batch.pop("labels")
                    predictions = pad_shard_unpad(p_eval_step)(
                        state, batch, min_device_batch=per_device_eval_batch_size
                    )
                    predictions = np.array(predictions)
                    labels[np.array(chain(*batch["attention_mask"])) == 0] = -100
                    preds, refs = get_labels(predictions, labels)
                    metric.add_batch(
                        predictions=preds,
                        references=refs,
                    )

                eval_metrics = compute_metrics()

                if data_args.return_entity_level_metrics:
                    logger.info(
                        f"Step... ({cur_step}/{total_steps} | Validation metrics: {eval_metrics}"
                    )
                else:
                    logger.info(
                        f"Step... ({cur_step}/{total_steps} | Validation f1: {eval_metrics['f1']}, Validation Acc:"
                        f" {eval_metrics['accuracy']})"
                    )

                if has_tensorboard and jax.process_index() == 0:
                    write_eval_metric(summary_writer, eval_metrics, cur_step)  # type: ignore

            if (cur_step % training_args.save_steps == 0 and cur_step > 0) or (
                cur_step == total_steps
            ):
                # save checkpoint after each epoch and push checkpoint to the hub
                if jax.process_index() == 0:
                    params = jax.device_get(unreplicate(state.params))
                    model.save_pretrained(training_args.output_dir, params=params)
                    tokenizer.save_pretrained(training_args.output_dir)
        epochs.desc = f"Epoch ... {epoch + 1}/{num_epochs}"

    # Eval on testing dataset after training
    if training_args.do_eval:
        eval_metrics = {}
        eval_loader = eval_data_collator(test_dataset, eval_batch_size)
        for batch in tqdm(
            eval_loader,
            total=len(test_dataset) // eval_batch_size,
            desc="Evaluating ...",
            position=2,
        ):
            labels = batch.pop("labels")
            predictions = pad_shard_unpad(p_eval_step)(
                state, batch, min_device_batch=per_device_eval_batch_size
            )
            predictions = np.array(predictions)
            labels[np.array(chain(*batch["attention_mask"])) == 0] = -100
            preds, refs = get_labels(predictions, labels)
            metric.add_batch(predictions=preds, references=refs)

        eval_metrics = compute_metrics()

        if jax.process_index() == 0:
            eval_metrics = {
                f"test_{metric_name}": value
                for metric_name, value in eval_metrics.items()
            }
            path = os.path.join(training_args.output_dir, "test_results.json")
            with open(path, "w") as f:
                json.dump(eval_metrics, f, cls=NumpyEncoder, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
