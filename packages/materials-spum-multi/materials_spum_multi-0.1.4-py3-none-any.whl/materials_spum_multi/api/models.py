from typing import Union
from enum import Enum
from dataclasses import dataclass


class Section(str, Enum):
    ABSTRACT = "abstract"
    CLAIM = "claim"
    DESCRIPTION = "description"


@dataclass
class Offset:
    start: int
    end: int
    text: str


@dataclass
class NormSubstanceResult:
    substance_offset: Offset
    substance_id: str | None = None
    entity_id: int | None = None

    def __post_init__(self):
        if self.substance_id is None and self.entity_id is None:
            raise ValueError("Either substance_id or entity_id must be provided.")


@dataclass
class NormPumResult:
    ppi_id: int
    ppi_tag_type: int
    raw_property: str
    property_offset: Offset
    measurement_min: float
    measurement_max: float
    raw_measurement: str
    measurement_offset: list[Offset]
    print_friendly_units: str
    raw_unit: str
    unit_offset: list[Offset]
    section: Section


@dataclass
class NormSubstancePumResult(NormSubstanceResult, NormPumResult):
    pass


NormSPUMResult = Union[NormSubstanceResult, NormPumResult, NormSubstancePumResult]


@dataclass
class SpumRequestInput:
    """
    Data class for input to the SPUM extraction API.
    """

    abstract: str = ""
    claims: str = ""
    description: str = ""
    is_splited: bool = False
    detailed: bool = False


@dataclass
class SpumRequestResponse:
    """
    Data class for output from the SPUM extraction API.
    """

    response: list[NormSPUMResult]
    ok: bool
    time: int
    message: str | None = None
    details: dict | None = None

    @classmethod
    def default(cls):
        return cls(
            response=[],
            ok=False,
            time=0,
            message="pass",
            details={},
        )
