import glob
from enum import Enum
from typing import Set

import pandas as pd
from loguru import logger


class SourceFormat(Enum):
    CSV = "csv"
    PARQUET = "parquet"


def _read_format(source_file_name: str, source_format: SourceFormat) -> pd.DataFrame:
    return (
        pd.read_parquet(source_file_name)
        if source_format == SourceFormat.PARQUET
        else pd.read_csv(source_file_name)
    )


def extract(
    data_dir: str,
    pattern: str,
    source_format: SourceFormat = SourceFormat.CSV,
    use_columns: Set = None,
) -> pd.DataFrame:
    """
    read dir with glob pattern and generate appended dataframe
    :param data_dir:
    :param pattern:
    :param source_format: PARQUET OR CSV (default)
    :return: concatenated df
    """
    extracted_df: pd.DataFrame = None
    for source_file_name in glob.glob(f"{data_dir}{pattern}"):
        logger.info(f"appending {source_file_name}")
        if extracted_df is None:
            extracted_df = _read_format(source_file_name, source_format)
        else:
            pd.concat(
                objs=[extracted_df, _read_format(source_file_name, source_format)],
                ignore_index=True,
            )
    logger.info(f"{len(extracted_df.index)} rows read")
    extracted_df = extracted_df.dropna()  # just to be sure!
    logger.info(f"{len(extracted_df.index)} rows after dropna")
    extracted_df = extracted_df.drop_duplicates()
    logger.info(f"{len(extracted_df.index)} rows after dedup ")
    return extracted_df
