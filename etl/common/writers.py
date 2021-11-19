import pandas as pd


def load(df: pd.DataFrame, target_file_name: str) -> None:
    """
    Not truely loaded into a db.
    Just for this case study a method for dumping result data.
    TODO: loaders for SQL DBs
    :param df:
    :param target_file_name:
    :return:
    """
    df.to_parquet(target_file_name)

