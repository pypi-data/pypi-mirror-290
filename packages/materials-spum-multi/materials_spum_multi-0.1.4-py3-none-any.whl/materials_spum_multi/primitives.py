from enum import Enum
from uuid import UUID
from dataclasses import dataclass


type PatentID = UUID


class Language(str, Enum):
    "Language of the text."

    EN = "en"
    ZH = "zh"


class Section(str, Enum):
    "Section of the patent, paper or grade."

    TITLE = "title"
    ABSTRACT = "abstract"
    CLAIM = "claim"
    DESCRIPTION = "description"
    IMAGE = "image"
    TABLE = "table"
    GRADE = "grade"


class MaterialsEntity(str, Enum):
    "Category of entity spans in materials."

    PRP = "property"
    MES = "measurement"
    UNT = "unit"
    CND = "condition"
    ENT = "entity"
    SBS = "substance"
    CMP = "composition"
    # auto label
    AUT = "auto"

    @property
    def bio_tag(self):
        return [f"B-{self.value}", f"I-{self.value}, O"]

    @property
    def id2label(self):
        return {i: label for i, label in enumerate(self.bio_tag)}

    @property
    def label2id(self):
        return {label: i for i, label in enumerate(self.bio_tag)}

    @classmethod
    def from_tag(cls, tag):
        return cls.__members__.get(tag.upper(), cls.AUT)


class MaterialsRelation(str, Enum):
    "Category of relations between entities in materials."

    E_SBS = "hasSubstance"
    E_CMP = "hasComposition"
    E_PRP = "hasProperty"
    P_ENT = "hasEntity"
    P_MES = "hasMeasurement"
    P_UNT = "hasUnit"
    P_CND = "hasCondition"
    AUT = "auto"

    @classmethod
    def from_tag(cls, tag):
        tag = list(filter(str.isalnum, tag))
        # make the 4th character upper case
        tag[3] = tag[3].upper()
        tag = "".join(tag)
        return cls(tag)


class TagStatus(str, Enum):
    """The status of the annotation tag."""

    PRELABELED = "prelabeled"
    ANNOTATED = "annotated"
    VERIFIED = "verified"
    ACCEPTED = "accepted"

    # parse from integer code to enum
    @classmethod
    def from_code(cls, code: int | None = None):
        if code is None:
            return cls.PRELABELED
        code2status = {
            0: cls.PRELABELED,
            1: cls.ANNOTATED,
            2: cls.VERIFIED,
            3: cls.ACCEPTED,
        }
        return code2status.get(code, cls.PRELABELED)


@dataclass
class Span:
    "Span of text annotated with a label."

    span_id: str
    start: int
    end: int
    span_text: str
    span_type: MaterialsEntity
    tag_status: TagStatus = TagStatus.PRELABELED

    def __post_init__(self):
        # sanity check
        assert self.start <= self.end, f"start: {self.start}, end: {self.end}"
        assert (
            len(self.span_text) == self.end - self.start
        ), f"span text length mismatch: {len(self.span_text)} != {self.end} - {self.start}"

    def __repr__(self):
        # hide start and end
        return f"Span(text={self.span_text}, label={self.span_type})"


@dataclass
class Relation:
    "Relation between two spans."

    span_left: Span
    span_right: Span
    relation_type: MaterialsRelation
