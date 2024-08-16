import click
from rich.console import Console
from rich.table import Table
from agentfud_password_manager.models import Entry, Session

@click.command()
def cli():
    """
    Lists all the entries
    """
    with Session() as session:
        entries = session.query(Entry).all()
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=4)
    table.add_column("Site URL")
    table.add_column("Username")
    table.add_column("Email")

    for entry in entries:
        table.add_row(
            str(entry.id),
            entry.site_url,
            entry.username,
            entry.email
        )

    console = Console()
    console.print(table)
