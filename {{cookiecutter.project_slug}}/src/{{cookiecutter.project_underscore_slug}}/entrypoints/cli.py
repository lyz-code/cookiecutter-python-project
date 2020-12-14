"""Command line interface definition."""

import click
from {{cookiecutter.project_underscore_slug}} import version
{% if cookiecutter.read_configuration_from_yaml == "True" %}
from {{cookiecutter.project_underscore_slug}}.entrypoints import load_config, load_logger
{% endif %}


@click.command()
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
def cli(ctx: Any, config_path: str, verbose: bool) -> None:
{%- else %}
def cli(verbose: bool) -> None:
{%- endif %}
    """Command line interface main click entrypoint."""
    {% if cookiecutter.read_configuration_from_yaml == "True" -%}
    ctx.obj["config"] = load_config(config_path)
    {%- endif %}
    load_logger(verbose)


if __name__ == "__main__":  # pragma: no cover
    cli()  # pylint: disable=E1120
