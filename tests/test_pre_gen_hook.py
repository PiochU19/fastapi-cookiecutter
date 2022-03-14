from pathlib import Path

import pandas as pd
import pytest
from hooks.pre_gen_project import (
    FILE_COLUMNS,
    FILE_NAME,
    post_processing_infomations,
    save_to_file,
)


@pytest.fixture
def csv_file():
    file_path = Path(FILE_NAME)
    tuple_of_data = ("one", "two", "three")
    post_processing_infomations.append(["old", "new", tuple_of_data])
    save_to_file()

    yield file_path

    file_path.unlink()


def test_save_to_file(csv_file: Path):
    assert csv_file.is_file()
    df = pd.read_csv(FILE_NAME)
    assert df.shape == (1, 3)
    assert tuple(df.columns) == FILE_COLUMNS
