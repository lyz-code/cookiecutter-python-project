"""Configuration tasks to be run before the template has been generated."""

import os


def main() -> None:
    """Run the pre hooks."""
    print(
        """
########################
# Pre generation hooks #
########################"""
    )


if __name__ == "__main__" and os.environ.get("COOKIECUTTER_TESTING") != "true":
    main()
