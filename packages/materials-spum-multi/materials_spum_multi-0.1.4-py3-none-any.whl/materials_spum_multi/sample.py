from dataclasses import dataclass
from uuid import UUID

from loguru import logger
from seqeval.scheme import IOB2, Tokens

from materials_spum_multi.primitives import MaterialsEntity, Section, Span
from materials_spum_multi.database import AutoModel
from materials_spum_multi.util import print_coloured_spans


BIO_TAGS = {
    "entity": "SUB",
    "property": "PRP",
    "unit": "UNT",
    "measurement": "MES",
}


@dataclass
class TokenLabelSamplePreTokenized(AutoModel):
    patent_id: UUID
    section: Section
    sentence_idx: int
    sent: list[str]
    ner_tags: list[str]

    def __post_init__(self):
        assert len(self.sent) == len(self.ner_tags)
        if len(self.sent) > 510:
            if set(self.ner_tags[510:]) == set(["O"]):
                self.sent = self.sent[:510]
                self.ner_tags = self.ner_tags[:510]
            elif set(self.ner_tags[:-510]) == set(["O"]):
                self.sent = self.sent[-510:]
                self.ner_tags = self.ner_tags[-510:]
            else:
                logger.warning(
                    f"Sequence too long: {len(self.sent)}: {self.patent_id}."
                )

    @property
    def text(self):
        return "".join(self.sent)

    def token2entity_span(self):
        tokens = Tokens(self.ner_tags, IOB2)
        raw_entities = tokens.entities
        return [
            Span(
                f"{self.patent_id}_{self.sentence_idx}",
                one.start,
                one.end,
                self.text[one.start : one.end],
                MaterialsEntity.from_tag(one.tag),
            )
            for one in raw_entities
        ]

    def inspect(self):
        all_spans = self.token2entity_span()
        curr = 0
        for one_span in all_spans:
            start, end, label = one_span.start, one_span.end, one_span.span_text
            if curr < start:
                # print(self.text[curr:start], end="")
                print_coloured_spans(self.text, curr, start, "")
            print_coloured_spans(self.text, start, end, label)
            curr = end
        if curr < len(self.text):
            # print(self.text[curr:len(self.text)])
            print_coloured_spans(self.text, curr, len(self.text), "")
