import sys

import cookiecutter.prompt


def set_number_of_workers():
    """Set number of workers if server was selected as gunicorn."""

    if "{{ cookiecutter.server }}" == "gunicorn":
        cookiecutter.prompt.read_user_variable("no_of_workers", 4)
    else:
        """{{ cookiecutter.update(
            {
                "no_of_workers": ""
            }
        )}}"""


def main():
    """Call all functions here."""

    set_number_of_workers()


if __name__ == "__main__":
    main()

    sys.exit(0)
