from typing import Optional

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.commands.services.hooks.slack_delete import slack_delete
from sym.flow.cli.commands.users.utils import get_or_prompt_service
from sym.flow.cli.errors import ReferencedObjectError
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand
from sym.flow.cli.helpers.utils import filter_dict
from sym.flow.cli.models.service import Service
from sym.flow.cli.models.service_type import ServiceType


def pre_service_delete_hooks(options: GlobalOptions, service: Service) -> None:
    """Registered hooks to call after before deletion of services"""

    if service.service_type == ServiceType.SLACK.type_name:
        slack_delete(options.sym_api, service.id)


@click.command(cls=TrackedCommand, name="delete", short_help="Delete an existing service")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--service-type",
    "_service_type",
    help="The service to delete",
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
def services_delete(
    options: GlobalOptions, _service_type: Optional[str], _external_id: Optional[str], force: bool
) -> None:
    """Set up a new service for your organization."""
    service = get_or_prompt_service(options.sym_api, _service_type, _external_id)

    # Prompt user to confirm
    if not force:
        click.confirm(
            "WARNING: This is a destructive action. \nAre you sure you want to continue?",
            abort=True,
            default=False,
        )

    active_references = filter_dict(options.sym_api.get_service_references(service.id), lambda refs: len(refs) > 0)
    if active_references:
        raise ReferencedObjectError(active_references)

    pre_service_delete_hooks(options, service)
    options.sym_api.delete_service(service.service_type, service.external_id)
    cli_output.success(
        f"Successfully deleted service type {service.service_type} with external ID {service.external_id}!"
    )
