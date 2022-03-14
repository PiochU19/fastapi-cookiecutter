import os
import sys
from ast import literal_eval
from typing import List, Tuple

import pandas as pd


FILE_COLUMNS = ("old_variable", "new_variable", "list_of_files")
FILE_NAME = "helper.csv"


def implode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Opposite of pandas explode function."""

    keys = [c for c in df if c != column]
    df = df.groupby(keys, as_index=False).agg({column: list})[df.columns]

    return df


def change_file_names() -> None:
    """Change names of the files that should be hidden from git by
    gitignore."""
    for root, _, files in os.walk("."):
        for file in files:
            if not file.endswith(".ignore"):
                continue

            path = os.path.join(root, file)
            os.rename(path, path[:-7])


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Process dataframe in order to open file only once."""

    vars_columns = [FILE_COLUMNS[0], FILE_COLUMNS[1]]

    # combinde old and new variable to tuple and drop
    df["vars_combined"] = df[vars_columns].apply(tuple, axis=1)
    df.drop(vars_columns, axis=1, inplace=True)

    # convert column from str to tuple
    df[FILE_COLUMNS[2]] = df[FILE_COLUMNS[2]].apply(literal_eval)

    # explode tuple of file paths and implode vars combined
    df = df.explode([FILE_COLUMNS[2]])
    df = implode(df, "vars_combined")

    df.rename({FILE_COLUMNS[2]: "file_path"}, axis=1, inplace=True)

    return df


def replace_old_vars_with_new_ones(df: pd.DataFrame) -> None:

    for _, row in df.iterrows():

        file_path: str = row[0]
        list_of_tuples_of_vars: List[Tuple[str | int]] = row[1]

        # fetch content of the file
        with open(file_path, "r") as read_file:
            file_content = read_file.read()

        # replace all variables in this file
        for old_var, new_var in list_of_tuples_of_vars:
            print("Replacing ", old_var, new_var)
            file_content = file_content.replace(str(old_var), str(new_var))

        # save processed content
        with open(file_path, "w") as write_file:
            write_file.write(file_content)


def main():
    """Call all functions here."""

    # read csv file and process
    df = pd.read_csv(FILE_NAME)
    df = process_dataframe(df)

    replace_old_vars_with_new_ones(df)

    os.remove(FILE_NAME)

    change_file_names()


if __name__ == "__main__":

    main()

    sys.exit(0)
