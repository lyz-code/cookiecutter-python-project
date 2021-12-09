"""Command line interface definition."""

import click

from .. import version
from ..config import Config
from . import load_logger

{% if cookiecutter.read_configuration_from_yaml == "True" %}
from click.core import Context

{% endif %}


@click.group()
@click.version_option(version="", message=version.version_info())
@click.option("-v", "--verbose", is_flag=True)
{% if cookiecutter.read_configuration_from_yaml == "True" %}
@click.option(
    "-c",
    "--config_path",
    default="~/.local/share/{{cookiecutter.project_underscore_slug}}/config.yaml",
    help="configuration file path",
    envvar="{{cookiecutter.project_underscore_slug | upper}}_CONFIG_PATH",
)
@click.pass_context
def cli(ctx: Context, config_path: str, verbose: bool) -> None:
{%- else %}
def cli(verbose: bool) -> None:
{%- endif %}
    """Command line interface main click entrypoint."""
    {% if cookiecutter.read_configuration_from_yaml == "True" -%}
    ctx.ensure_object(dict)

    ctx.obj["config"] = Config().load(config_path)

    {%- endif %}
    load_logger(verbose)

@cli.command(hidden=True)
def null() -> None:
    """Do nothing.

    Used for the tests until we have a better solution.
    """

if __name__ == "__main__":  # pragma: no cover
    # E1120: As the arguments are passed through the function decorators instead of
    # during the function call, pylint get's confused.
    cli(ctx={})  # noqa: E1120
