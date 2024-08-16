import jax
import jax.numpy as jnp
import flax.linen as nn
from flax.training import train_state
import numpy as np
from tqdm import tqdm
from transformers import FlaxRobertaModel


class CRF(nn.Module):
    num_tags: int

    def setup(self):
        self.transitions = self.param(
            "transitions", nn.initializers.uniform(), (self.num_tags, self.num_tags)
        )

    def __call__(self, emissions, tags, mask):
        log_likelihood, _ = self.crf_forward(emissions, tags, mask)
        return log_likelihood

    def crf_forward(self, emissions, tags, mask):
        seq_length = emissions.shape[1]

        score = self.transitions[tags[:, 0]]
        score += emissions[:, 0]

        for i in range(1, seq_length):
            mask_t = jnp.expand_dims(mask[:, i], axis=1)
            emit_t = emissions[:, i]
            trans_t = self.transitions[tags[:, i - 1], tags[:, i]]
            score = score + trans_t * mask_t + emit_t * mask_t

        return score.sum(), tags


class BiLSTMCRF(nn.Module):
    hidden_dim: int
    num_tags: int

    def setup(self):
        self.lstm = nn.scan(nn.LSTMCell, in_axes=1, out_axes=1)(
            name="lstm", num_features=self.hidden_dim
        )
        self.hidden2tag = nn.Dense(self.num_tags)
        self.crf = CRF(self.num_tags)

    def __call__(self, inputs, tags=None, mask=None, train=True):
        hidden, _ = self.lstm(inputs)
        emissions = self.hidden2tag(hidden)

        if train and tags is not None and mask is not None:
            crf_score = self.crf(emissions, tags, mask)
            return crf_score
        else:
            return emissions


class RobertaBiLSTMCRF(nn.Module):
    num_tags: int
    hidden_dim: int
    roberta_model_name: str

    def setup(self):
        self.roberta = FlaxRobertaModel.from_pretrained(self.roberta_model_name)
        self.bilstmcrf = BiLSTMCRF(hidden_dim=self.hidden_dim, num_tags=self.num_tags)

    def __call__(self, input_ids, attention_mask, labels=None, mask=None, train=True):
        # Obtain hidden states from RoBERTa
        outputs = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        sequence_output = outputs.last_hidden_state

        # Apply BiLSTM-CRF layer
        if labels is not None and mask is not None:
            logits = self.bilstmcrf(sequence_output, labels, mask, train=train)
        else:
            logits = self.bilstmcrf(sequence_output, train=train)

        return logits


def create_train_state(rng, model, learning_rate, input_shape, mask_shape):
    params = model.init(
        rng, input_ids=jnp.ones(input_shape), attention_mask=jnp.ones(mask_shape)
    )["params"]
    tx = optax.adam(learning_rate)
    return train_state.TrainState.create(apply_fn=model.apply, params=params, tx=tx)


def train_step(state, batch):
    input_ids, attention_mask, labels, mask = batch

    def loss_fn(params):
        logits = state.apply_fn(
            {"params": params}, input_ids, attention_mask, labels, mask
        )
        return -logits.sum()  # Negative log likelihood for maximization

    grad_fn = jax.value_and_grad(loss_fn)
    loss, grads = grad_fn(state.params)
    state = state.apply_gradients(grads=grads)
    metrics = {"loss": loss}
    return state, metrics


def train_model(state, train_data, num_epochs):
    for epoch in range(num_epochs):
        epoch_loss = 0
        for batch in tqdm(train_data):
            state, metrics = train_step(state, batch)
