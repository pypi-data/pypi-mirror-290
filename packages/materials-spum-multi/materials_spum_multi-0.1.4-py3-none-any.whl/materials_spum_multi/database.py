from dataclasses import asdict, dataclass


@dataclass
class AutoModel:
    """Base class for auto model."""

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict):
        # only parse from keys in the dataclass
        d = {k: v for k, v in d.items() if k in cls.__dataclass_fields__}
        return cls(**d)


@dataclass
class EntityModel(AutoModel):
    display_name_cn: str
    display_name_en: str
    alias_list_cn: list[str]
    alias_list_en: list[str]

    def __post_init__(self):
        self.alias_list_cn = (
            [] if self.alias_list_cn is None else list(self.alias_list_cn)
        )
        self.alias_list_en = (
            [] if self.alias_list_en is None else list(self.alias_list_en)
        )


@dataclass
class PropertyEntity(EntityModel):
    """Property entity data."""

    ppi_id: int
    print_friendly_units: str
    lower_bound: float
    upper_bound: float
    class_i_name: str
    unit_recognition: bool = False

    def __post_init__(self):
        super().__post_init__()


@dataclass
class SubstanceEntity(EntityModel):
    """Substance entity data."""

    substance_id: str
    cas_rn: list[str]
    inchi: str
    mol_formula: str
    molecular_formula: str
    cas_formula: list[str]

    def __post_init__(self):
        super().__post_init__()

@dataclass
class BodyEntity(EntityModel):
    """Body entity data."""

    ppi_id: int
    category: str
    short_name_en: list[str]
    short_name_cn: list[str]

    def __post_init__(self):
        super().__post_init__()
        self.short_name_en = (
            [] if self.short_name_en is None else list(self.short_name_en)
        )
        self.short_name_cn = (
            [] if self.short_name_cn is None else list(self.short_name_cn)
        )
        self.alias_list_en.extend(self.short_name_en)
        self.alias_list_cn.extend(self.short_name_cn)
