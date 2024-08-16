from dataclasses import dataclass, field
from uuid import UUID

from loguru import logger
import re

from materials_spum_multi.primitives import (
    MaterialsEntity,
    MaterialsRelation,
    TagStatus,
    Section,
    Relation,
    Span,
)
from materials_spum_multi.database import AutoModel
from materials_spum_multi.sample import TokenLabelSamplePreTokenized, BIO_TAGS
from materials_spum_multi.util import clean_text, print_coloured_spans


# initiate the logger for this module
logger = logger.bind(name=__name__)


@dataclass
class TokenLabelAnnotated(AutoModel):
    "The annotated data from a sequence labeling task."

    task_name: str
    patent_id: UUID
    section: Section
    text: str
    is_cleaned: bool = False
    entities: list[Span] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    validated: bool = field(default=False)

    def inspect(
        self,
        skip_entities: bool = False,
    ):
        if skip_entities:
            all_spans = [
                ent for ent in self.entities if ent.span_type != MaterialsEntity.ENT
            ]
        else:
            all_spans = self.entities

        curr = 0
        for one_span in all_spans:
            start, end, label = one_span.start, one_span.end, one_span.span_type
            if curr < start:
                # print(self.text[curr:start], end="")
                print_coloured_spans(self.text, curr, start, "")
            print_coloured_spans(self.text, start, end, label)
            curr = end
        if curr < len(self.text):
            # print(self.text[curr:len(self.text)])
            print_coloured_spans(self.text, curr, len(self.text), "")

    @staticmethod
    def span_overlap(span, span_list):
        for s in span_list:
            if max(span.start, s.start) < min(span.end, s.end):
                return True
        return False

    def into_samples(
        self, split_pat: re.Pattern[str]
    ) -> list[TokenLabelSamplePreTokenized]:
        samples = []
        tokens = list(self.text)
        pid = self.patent_id
        section = self.section
        labels = ["O"] * len(tokens)
        for ent in self.entities:
            if ent.span_type not in BIO_TAGS:
                continue
            labels[ent.start] = "B-" + BIO_TAGS[ent.span_type]
            for i in range(ent.start + 1, ent.end):
                labels[i] = "I-" + BIO_TAGS[ent.span_type]
        # find the sentences
        start_matches = [m.start() for m in re.finditer(split_pat, self.text)]
        start_matches.append(-1)
        for idx, curr in enumerate(start_matches):
            if curr == -1:
                break
            next = start_matches[idx + 1]
            sent = tokens[curr:next]
            label = labels[curr:next]
            sample = TokenLabelSamplePreTokenized(
                pid,
                section,
                idx,
                sent,
                label,
            )
            samples.append(sample)

        return samples

    def __post_init__(self):
        self.is_cleaned = self.text == clean_text(self.text)
        self.validated = (
            all([ent.tag_status != "prelabeled" for ent in self.entities])
            and len(self.entities) > 0
        )

    @classmethod
    def from_dict(cls, d: dict):
        # only parse from keys in the dataclass
        d = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        d["entities"] = [Span(**ent) for ent in d["entities"]]
        d["relations"] = [Relation(**rel) for rel in d["relations"]]
        obj = cls(**d)
        return obj


@dataclass
class DataCurationAnnotatedResult:
    dc_id: int
    patent_id: UUID
    text: str
    tags: list[dict]
    entities: list[Span] = field(init=False)
    relations: list[Relation] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.id2entities = {}
        self.tag_count = len(self.tags)

        for tag in self.tags:
            one_span = Span(
                span_id=str(tag["tagItemId"]),
                start=tag["startIndex"],
                end=tag["endIndex"],
                span_text=tag["text"],
                span_type=MaterialsEntity(tag["tagName"].lower()),
                tag_status=TagStatus.from_code(tag["tagShadowType"]),
            )
            self.id2entities.update({one_span.span_id: one_span})
        logger.info(
            f"Created {len(self.id2entities)} entities from annotation for patent {self.patent_id}."
        )
        # process the relations after all entities are created
        for tag in self.tags:
            if "line" in tag:
                lines = tag["line"]
                for line in lines:
                    one_relation = Relation(
                        span_left=self.id2entities[str(tag["tagItemId"])],
                        span_right=self.id2entities[str(line["id"])],
                        relation_type=MaterialsRelation.from_tag(line["name"]),
                    )
                    self.relations.append(one_relation)
        logger.info(
            f"Created {len(self.relations)} relations from annotation for patent {self.patent_id}."
        )
        # restore entities as a list
        self.entities = list(self.id2entities.values())

    def into_result(self, task_name: str, section: Section) -> TokenLabelAnnotated:
        return TokenLabelAnnotated(
            task_name=task_name,
            patent_id=self.patent_id,
            section=section,
            text=self.text,
            entities=self.entities,
            relations=self.relations,
        )
