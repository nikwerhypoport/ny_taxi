import glob
from typing import Set

import pandas as pd


COLUMNS_OF_INTEREST = {
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "PULocationID",
    "DOLocationID",
}

DATA_DIR = "resources/data/"

def preprocess(lookup_table: pd.DataFrame) -> None:
    for source_file_name in glob.glob(f"{DATA_DIR}/*tripdata*.csv"):
        df: pd.DataFrame = pd.read_csv(source_file_name)
        df = _transform(df, lookup_table)
        target_file_name = f"{source_file_name}.parquet"
        df.to_parquet(target_file_name)


def _transform(df: pd.DataFrame, lookup_table: pd.DataFrame) -> pd.DataFrame:
    enriched_df: pd.DataFrame = _drop_cols(df=df, cols_to_keep=COLUMNS_OF_INTEREST)
    enriched_df = _enrich_locations(enriched_df, lookup_table)
    enriched_df = _extract_year_month(enriched_df)
    return enriched_df

def _extract_year_month(df: pd.DataFrame) -> pd.DataFrame:
    df['year'] = df['tpep_dropoff_datetime'].str.extract("^(\d+).*")
    df['month'] = df['tpep_dropoff_datetime'].str.extract("^\d+-(\d+).*")
    df = df.assign(month=df.year + "-" + df.month)
    df = df.drop(columns=["year"], axis=1)
    return df

def _enrich_locations(df: pd.DataFrame, lookup_table: pd.DataFrame) -> pd.DataFrame:
    enriched_df = _enrich_pickup_location(df, lookup_table)
    enriched_df = _enrich_drop_off_location(enriched_df, lookup_table)
    enriched_df = enriched_df.drop(columns=["LocationID_y", "LocationID_x"], axis=1)
    return enriched_df


def _enrich_drop_off_location(
    df: pd.DataFrame, lookup_table: pd.DataFrame
) -> pd.DataFrame:
    enriched_df = pd.merge(
        df, lookup_table, how="left", left_on="DOLocationID", right_on="LocationID"
    )
    enriched_df = enriched_df.rename(columns={"Borough": "drop_off_borough", "Zone": "drop_off_zone"})
    enriched_df = enriched_df.drop(["DOLocationID", "service_zone"], axis=1)
    return enriched_df


def _enrich_pickup_location(
    df: pd.DataFrame, lookup_table: pd.DataFrame
) -> pd.DataFrame:
    enriched_df = pd.merge(
        df, lookup_table, how="left", left_on="PULocationID", right_on="LocationID"
    )
    enriched_df = enriched_df.rename(columns={"Borough": "pickup_borough", "Zone": "pickup_zone"})
    enriched_df = enriched_df.drop(["PULocationID", "service_zone"], axis=1)
    return enriched_df


def _drop_cols(df: pd.DataFrame, cols_to_keep: Set) -> pd.DataFrame:
    columns_to_drop: Set = _get_columns_to_drop(set(df.columns), cols_to_keep)
    df = df.drop(columns_to_drop, axis=1)
    return df


def _get_columns_to_drop(columns: Set, cols_to_keep: Set) -> Set:
    diff = cols_to_keep.symmetric_difference(columns)
    return diff


def read_lookup_table() -> pd.DataFrame:
    return pd.read_csv(f"{DATA_DIR}/taxi+_zone_lookup.csv")


if __name__ == "__main__":
    """
    Small helper script for making life easier when dealing with huge csv files which need to be read constantly
    - to parquet for speed
    - drop unnecessary columns for the task
    - enrich necessary columns for the task
    - writes target files to directory where files are read from
    This would be integrated as a preprocessing step in a production system
    """

    lookup_df = read_lookup_table()
    preprocess(lookup_df)
