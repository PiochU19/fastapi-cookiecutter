from pathlib import Path

import pandas as pd
import pytest
from hooks.post_gen_project import process_dataframe
from hooks.pre_gen_project import (
    FILE_NAME,
    post_processing_infomations,
    save_to_file,
)


@pytest.fixture(name="result_df")
def create_result_dataframe():

    post_processing_infomations.append(
        ("new_var", "old_var", ("first_file.py", "second_file.py"))
    )
    post_processing_infomations.append(
        ("second_new_var", "second_old_var", ("second_file.py", "third_file.py"))
    )
    save_to_file()

    yield

    post_processing_infomations.clear()
    Path(FILE_NAME).unlink()


def test_process_dataframe(result_df: None):

    df = pd.read_csv(FILE_NAME)
    assert df.shape == (2, 3)

    df = process_dataframe(df)
    assert df.shape == (3, 2)

    values = [
        ["first_file.py", [("new_var", "old_var")]],
        [
            "second_file.py",
            [("new_var", "old_var"), ("second_new_var", "second_old_var")],
        ],
        ["third_file.py", [("second_new_var", "second_old_var")]],
    ]
    new_df = pd.DataFrame(values, columns=df.columns)

    result = df.compare(new_df)

    assert result.empty
