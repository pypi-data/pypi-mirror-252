from typing import Optional

import click

from sym.flow.cli.commands.users.utils import get_or_prompt_service
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.identity_operations import delete_identity
from sym.flow.cli.helpers.tracked_command import TrackedCommand


@click.command(
    cls=TrackedCommand,
    name="delete-identity",
    short_help="Delete an Identity for a Bot",
)
@click.argument("username", required=True, type=str)
@click.option(
    "--service-type",
    "_service_type",
    help="The type of service the identity is tied to",
)
@click.option(
    "--external-id",
    "_external_id",
    help="The identifier for the service",
)
@click.option(
    "--force",
    is_flag=True,
    help="Delete the service immediately",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def delete_bot_identity(
    options: GlobalOptions,
    username: str,
    _service_type: Optional[str],
    _external_id: Optional[str],
    force: bool,
) -> None:
    """For an existing Sym Bot, delete a single Identity such as an AWS SSO Principal UUID or a Slack User ID.

    \b
    Example:
        `symflow bots delete-identity hal`

    """
    original_user = options.sym_api.get_bot(username)
    service = get_or_prompt_service(options.sym_api, _service_type, _external_id)

    # Prompt user to confirm
    if not force:
        click.confirm(
            "WARNING: This is a destructive action. \nAre you sure you want to continue?",
            abort=True,
            default=False,
        )

    delete_identity(options, original_user, service)
