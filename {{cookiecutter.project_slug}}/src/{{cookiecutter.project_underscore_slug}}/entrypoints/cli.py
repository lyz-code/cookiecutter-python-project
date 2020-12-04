"""Command line interface definition."""

import click
from {{cookiecutter.project_underscore_slug}} import version


@click.command()
@click.version_option(version="", message=version.version_info())
def cli() -> None:
    """Command line interface main click entrypoint."""


if __name__ == "__main__":  # pragma: no cover
    cli()  # pylint: disable=E1120
