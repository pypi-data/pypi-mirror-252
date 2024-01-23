import click

from sym.flow.cli.commands.resources.list import resources_list
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.group(name="resources", short_help="Perform operations on Sym resources")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def resources(options: GlobalOptions) -> None:
    """Operations on resources (e.g. sym_flow)

    Currently, only supports the `list` operation. Any other operation (e.g. `create`
    or `update`) should be performed using Terraform.

    For more information, see https://docs.symops.com/docs/terraform-provider
    """


resources.add_command(resources_list)
