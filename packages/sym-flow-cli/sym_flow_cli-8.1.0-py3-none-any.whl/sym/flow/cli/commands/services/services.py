import click

from sym.flow.cli.commands.services.services_delete import services_delete
from sym.flow.cli.commands.services.services_list import services_list
from sym.flow.cli.commands.services.services_update import services_update
from sym.flow.cli.helpers.global_options import GlobalOptions


@click.group(name="services", short_help="Perform operations on Sym Services")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def services(options: GlobalOptions) -> None:
    """Operations on Services"""


services.add_command(services_update)
services.add_command(services_list)
services.add_command(services_delete)
