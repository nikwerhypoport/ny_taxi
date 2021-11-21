import pandas as pd
from pandasql import sqldf

from etl.common.readers import extract, SourceFormat
from etl.common.writers import load

DATA_DIR = "resources/data/"


def _grouping(source_df: pd.DataFrame) -> pd.DataFrame:
    """
    grouping and aggregation of passenger counts by month, pickup_zone, drop_off_zone
    :param source_df:
    :return:
    """
    query = """
                    SELECT sum(passenger_count) as count, 
                           pickup_zone, 
                           drop_off_zone, 
                           month 
                    FROM source_df 
                    GROUP BY month, pickup_zone, drop_off_zone
                """
    grouped_df = sqldf(query, locals())
    return grouped_df


def _ranking(source_df: pd.DataFrame) -> pd.DataFrame:
    """
    rank by k=50 per pickup_zone and month
    :param source_df:
    :return:
    """
    source_df["rank"] = source_df.groupby(["pickup_zone", "month"])["count"].rank(
        method="max", ascending=False
    )
    ranked = source_df[source_df["rank"] <= 50.0]
    return ranked


def _transform(source_df: pd.DataFrame) -> pd.DataFrame:
    grouped_df = _grouping(source_df)
    ranked_df = _ranking(grouped_df)
    return ranked_df


def run():
    df: pd.DataFrame = extract(
        DATA_DIR, "enriched_trip_data.parquet", SourceFormat.PARQUET
    )
    df = _transform(df)
    load(df, f"{DATA_DIR}ranked_by_month_and_pu_zone.parquet")


if __name__ == "__main__":
    """
    Second Task for an Airflow DAG
    - read parquet from before (extract)
    - group/rank (transform)
    - write to parquet again (load)
    This would be integrated as a preprocessing step in a production system, for example as the second
    step in an Airflow DAG.
    """
    run()
