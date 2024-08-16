from typing import Type
import os
from dotenv import load_dotenv
import pandas as pd

from dadude.reader.delta_client import read_delta_table
from materials_spum_multi.annotation import TokenLabelAnnotated
from materials_spum_multi.sample import TokenLabelSamplePreTokenized
from materials_spum_multi.database import (
    AutoModel,
    PropertyEntity,
    SubstanceEntity,
    BodyEntity,
)


load_dotenv()
STORAGE_BUCKET_PREFIX = os.getenv("STORAGE_BUCKET_PREFIX")


def dataframe_orm(df: pd.DataFrame, orm: Type[AutoModel]) -> list[AutoModel]:
    return [orm.from_dict(row) for row in df.to_dict(orient="records")]


def load_asset_collection(table_path: str, asset: Type[AutoModel]) -> list[AutoModel]:
    # need to set environment variables for `default_storage_config`
    table = read_delta_table(table_path)
    collection = dataframe_orm(table, asset)
    return collection


property_entity_collection = load_asset_collection(
    f"{STORAGE_BUCKET_PREFIX}/gold/material_property_entity_v3",
    PropertyEntity,
)

body_entity_collection = load_asset_collection(
    f"{STORAGE_BUCKET_PREFIX}/bronze/materials_body_entity",
    BodyEntity,
)

substance_entity_collection = load_asset_collection(
    f"{STORAGE_BUCKET_PREFIX}/silver/cheman_substance_entity",
    SubstanceEntity,
)

dc_annotation_spum_cn_clms_2407_collection = load_asset_collection(
    f"{STORAGE_BUCKET_PREFIX}/bronze/dc_annotation_spum_cn_clms_2407/",
    TokenLabelAnnotated,
)

dc_annotation_spum_cn_desc_2407_collection = load_asset_collection(
    f"{STORAGE_BUCKET_PREFIX}/bronze/dc_annotation_spum_cn_desc_2407/",
    TokenLabelAnnotated,
)

spum_dc_annotation_samples_2408 = load_asset_collection(
    f"{STORAGE_BUCKET_PREFIX}/silver/spum_dc_annotation_samples_2408/",
    TokenLabelSamplePreTokenized,
)

# TODO: add description annotations
# TODO: add previous batch of annotations
