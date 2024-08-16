import click
import pkg_resources
from rich.console import Console
from rich.table import Table

@click.command()
def cli():
    """
    AgentFUD Password Manager version and project info
    """
    version = pkg_resources.require("af-password-manager")[0].version
    table = Table(show_header=False)
    table.add_row("password_manager_version", version)
    table.add_row("Python package", "https://pypi.org/project/agentfud-password-manager")
    table.add_row("Repository", "https://github.com/AgentFUD/agentfud-password-manager")
    table.add_row("Issues", "https://github.com/AgentFUD/agentfud-password-manager/issues")
    table.add_row("Contact", "agentfud@gmail.com")
    console = Console()
    console.print(table)