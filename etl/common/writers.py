import pandas as pd


def load(df: pd.DataFrame, target_file_name: str):
    df.to_parquet(target_file_name)
    # TODO: loaders for SQL DBs
