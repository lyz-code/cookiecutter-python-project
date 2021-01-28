"""Define the different ways to expose the program functionality.

Functions:
    load_logger: Configure the Logging logger.
"""

import logging
import sys
{% if cookiecutter.read_configuration_from_yaml == "True" %}
from {{cookiecutter.project_underscore_slug}}.config import Config, ConfigError
from ruamel.yaml.parser import ParserError
{% endif %}

log = logging.getLogger(__name__)


{% if cookiecutter.read_configuration_from_yaml == "True" %}
def load_config(config_path: str) -> Config:
    """Load the configuration from the file."""
    log.debug(f"Loading the configuration from file {config_path}")
    try:
        config = Config(config_path)
    except ConfigError as error:
        log.error(f"Configuration Error: {str(error)}")
        sys.exit(1)
    except FileNotFoundError:
        log.error(f"Error opening configuration file {config_path}")
        sys.exit(1)

    return config


{% endif %}
# I have no idea how to test this function :(. If you do, please send a PR.
def load_logger(verbose: bool = False) -> None:  # pragma no cover
    """Configure the Logging logger.

    Args:
        verbose: Set the logging level to Debug.
    """
    logging.addLevelName(logging.INFO, "[\033[36m+\033[0m]")
    logging.addLevelName(logging.ERROR, "[\033[31m+\033[0m]")
    logging.addLevelName(logging.DEBUG, "[\033[32m+\033[0m]")
    logging.addLevelName(logging.WARNING, "[\033[33m+\033[0m]")
    if verbose:
        logging.basicConfig(
            stream=sys.stderr, level=logging.DEBUG, format="  %(levelname)s %(message)s"
        )
    else:
        logging.basicConfig(
            stream=sys.stderr, level=logging.INFO, format="  %(levelname)s %(message)s"
        )
