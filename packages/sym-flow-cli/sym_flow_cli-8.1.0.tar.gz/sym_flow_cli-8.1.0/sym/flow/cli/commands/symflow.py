import os

import click

from sym.flow.cli.commands.bots import bots_commands
from sym.flow.cli.commands.config import config_commands
from sym.flow.cli.commands.docs import docs
from sym.flow.cli.commands.domains import domains_commands
from sym.flow.cli.commands.generate import generate
from sym.flow.cli.commands.init import init
from sym.flow.cli.commands.login import login, logout
from sym.flow.cli.commands.migrate import migrate
from sym.flow.cli.commands.organization import organization_commands
from sym.flow.cli.commands.resources import resources_commands
from sym.flow.cli.commands.services import services_commands
from sym.flow.cli.commands.status import status
from sym.flow.cli.commands.tokens import tokens_commands
from sym.flow.cli.commands.users import users_commands
from sym.flow.cli.commands.version import version
from sym.flow.cli.helpers.constants import DEFAULT_API_URL, DEFAULT_AUTH_URL, SentryDSN
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.sentry import setup_sentry
from sym.flow.cli.helpers.version import maybe_display_update_message
from sym.flow.cli.version import __version__


@click.group(name="symflow", context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--debug", is_flag=True, help="enable verbose debugging", envvar="SYM_DEBUG")
@click.option(
    "--api-url",
    default=DEFAULT_API_URL,
    help="set the Sym API URL",
    envvar="SYM_API_URL",
)
@click.option(
    "--auth-url",
    default=DEFAULT_AUTH_URL,
    help="set the Sym auth url",
    envvar="SYM_AUTH_URL",
)
@click.version_option(version=__version__, message="%(version)s")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@setup_sentry(dsn=SentryDSN, release=f"sym-flow-cli@{__version__}")
def symflow(options: GlobalOptions, auth_url: str, api_url: str, debug: bool) -> None:
    """
    Manage Sym Services and Users in your organization

    https://docs.symops.com/docs/using-the-symflow-cli
    """

    options.debug = debug
    if sym_jwt := os.getenv("SYM_JWT"):
        options.set_access_token(sym_jwt)
    options.set_api_url(api_url)
    options.set_auth_url(auth_url)
    options.dprint(f"SYM_AUTH_URL={auth_url}, SYM_API_URL={api_url}")

    maybe_display_update_message()


symflow.add_command(version)
symflow.add_command(login)
symflow.add_command(logout)
symflow.add_command(status)
symflow.add_command(init)
symflow.add_command(organization_commands)
symflow.add_command(generate)
symflow.add_command(services_commands)
symflow.add_command(users_commands)
symflow.add_command(config_commands)
symflow.add_command(tokens_commands)
symflow.add_command(bots_commands)
symflow.add_command(resources_commands)
symflow.add_command(domains_commands)
symflow.add_command(docs)
symflow.add_command(migrate)
