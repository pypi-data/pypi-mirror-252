import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand
from sym.flow.cli.models import ServiceType
from sym.flow.cli.models.service import BaseService
from sym.flow.cli.models.user import CSVMatcher


@click.command(
    cls=TrackedCommand,
    name="delete",
    short_help="Delete a User",
)
@click.argument("email", required=True, type=str)
@click.option(
    "--force",
    is_flag=True,
    help="Delete the user immediately",
)
@click.make_pass_decorator(GlobalOptions, ensure=True)
def users_delete(options: GlobalOptions, email: str, force: bool) -> None:
    # Prompt user to confirm
    if not force:
        click.confirm(
            "WARNING: This is a destructive action. \nAre you sure you want to continue?",
            abort=True,
            default=False,
        )

    # External ID is not used, using service as a placeholder
    service_obj = BaseService(slug=ServiceType.SYM.type_name, external_id="cloud")
    matcher = CSVMatcher(service=service_obj, value=email)

    payload = {
        "users": [
            {
                "identity": {
                    "service_type": ServiceType.SYM.type_name,
                    "matcher": matcher.to_dict(),
                },
            }
        ]
    }

    options.sym_api.delete_user(payload)
    cli_output.success(f"Successfully deleted user {email}!")
