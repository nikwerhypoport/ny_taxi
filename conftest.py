from pathlib import Path

from _pytest.config import Config


def pytest_configure(config: Config):
    cwd = Path.cwd()
    cwd.joinpath("etl")