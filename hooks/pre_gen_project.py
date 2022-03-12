from __future__ import print_function
import os
import sys
from typing import List, Tuple

import cookiecutter.prompt
import pandas as pd


FILE_COLUMNS = ("old_variable", "new_variable", "list_of_files")
FILE_NAME = "helper.csv"

post_processing_infomations: List[Tuple[str]] = []
project_slug = "{{ cookiecutter.project_slug }}"


def save_to_file() -> None:
    """Saves needed informations to csv, to make post processing."""

    df = pd.DataFrame(post_processing_infomations, columns=FILE_COLUMNS)
    df.to_csv(FILE_NAME, index=False)


def append_post_processing_informations(
    old_var: str, new_var: str, tuple_of_files: Tuple[str]
) -> None:
    """In order to make post processing, we need to save metadata informations
    by appending to list, and saving to file at the end."""

    # to avoid any naming collision
    old_var = project_slug + old_var

    post_processing_infomations.append((old_var, new_var, tuple_of_files))


def set_number_of_workers() -> None:
    """Set number of workers if server was selected as gunicorn."""

    if "{{ cookiecutter.server }}" == "gunicorn":
        no_of_workers = str(
            cookiecutter.prompt.read_user_variable("no_of_workers", "4")
        )

        "{{ cookiecutter.update({'no_of_workers': cookiecutter.project_slug + 'no_of_workers' }) }}"

        tuple_of_affected_files = (os.path.join("docker", "develop", "entrypoint.sh"),)
        append_post_processing_informations(
            "no_of_workers", no_of_workers, tuple_of_affected_files
        )


def main():
    """Call all functions here."""

    set_number_of_workers()

    save_to_file()


if __name__ == "__main__":
    main()

    sys.exit(0)
