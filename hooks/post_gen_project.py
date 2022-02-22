from ast import literal_eval

import pandas as pd


FILE_COLUMNS = ("old_variable", "new_variable", "list_of_files")
FILE_NAME = "helper.csv"


def implode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Opposite of pandas explode function."""

    keys = [c for c in df if c != column]
    df = df.groupby(keys, as_index=False).agg({column: list})[df.columns]

    return df


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


def main():
    ...


if __name__ == "__main__":
    ...
    # main()
