from typing import Set

import pandas as pd

from common.readers import extract, SourceFormat
from common.writers import load

COLUMNS_OF_INTEREST = {
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "PULocationID",
    "DOLocationID",
}

# TODO: needs to be parameterized in a prod env
DATA_DIR = "resources/data/"


def _transform(df: pd.DataFrame, lookup_table: pd.DataFrame) -> pd.DataFrame:
    enriched_df: pd.DataFrame = _drop_cols(df=df, cols_to_keep=COLUMNS_OF_INTEREST)
    enriched_df = enriched_df.dropna()
    enriched_df = _enrich_locations(enriched_df, lookup_table)
    enriched_df = _extract_year_month(enriched_df)
    return enriched_df


def _extract_year_month(df: pd.DataFrame) -> pd.DataFrame:
    repl = lambda m: f"{m.group(1)}-{m.group(2)}"
    df["month"] = df["tpep_dropoff_datetime"].str.replace(
        "^(\d+)-(\d+).*", repl, regex=True
    )
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
    enriched_df = enriched_df.rename(
        columns={"Borough": "drop_off_borough", "Zone": "drop_off_zone"}
    )
    enriched_df = enriched_df.drop(["DOLocationID", "service_zone"], axis=1)
    return enriched_df


def _enrich_pickup_location(
    df: pd.DataFrame, lookup_table: pd.DataFrame
) -> pd.DataFrame:
    enriched_df = pd.merge(
        df, lookup_table, how="left", left_on="PULocationID", right_on="LocationID"
    )
    enriched_df = enriched_df.rename(
        columns={"Borough": "pickup_borough", "Zone": "pickup_zone"}
    )
    enriched_df = enriched_df.drop(["PULocationID", "service_zone"], axis=1)
    return enriched_df


def _drop_cols(df: pd.DataFrame, cols_to_keep: Set) -> pd.DataFrame:
    columns_to_drop: Set = _get_columns_to_drop(set(df.columns), cols_to_keep)
    df = df.drop(columns_to_drop, axis=1)
    return df


def _get_columns_to_drop(columns: Set, cols_to_keep: Set) -> Set:
    diff = cols_to_keep.symmetric_difference(columns)
    return diff


def run() -> None:
    lookup_df = extract(DATA_DIR, "taxi+_zone_lookup.csv", SourceFormat.CSV)
    df: pd.DataFrame = extract(DATA_DIR, "*tripdata*.csv", SourceFormat.CSV)
    df = _transform(df, lookup_df)
    load(df, f"{DATA_DIR}/enriched_trip_data.parquet")


if __name__ == "__main__":
    """
    First Task for an Airflow DAG
    - to parquet (load speedup)
    - drop unnecessary columns for next tasks (memory)
    - enrich necessary columns for the task (processing time)
    - writes target files to directory where files are read from
    This would be integrated as a preprocessing step in a production system, for example as the first
    step in an Airflow DAG.
    """
    run()
