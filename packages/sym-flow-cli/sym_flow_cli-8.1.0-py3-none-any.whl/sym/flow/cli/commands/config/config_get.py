"""Config Get

Retrieve a value from the Sym Flow config.
"""


import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand


@click.command(cls=TrackedCommand, name="get", short_help="Get a config value")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.argument("key")
def config_get(options: GlobalOptions, key: str) -> None:
    """Get a config value from your local Sym Flow config file.
    Nested configs can be accessed by a dot-separated path
    e.g. `symflow config get auth_token.access_token`
    """
    # For internal use only
    try:
        value = Config.get_value(key)
    except ValueError:
        cli_output.fail(f"The path '{key}' is incomplete", "Please enter a full path")

    if not value:
        cli_output.fail(f"Failed to get config value for '{key}'", "The key doesn't exist")

    cli_output.info(value)
