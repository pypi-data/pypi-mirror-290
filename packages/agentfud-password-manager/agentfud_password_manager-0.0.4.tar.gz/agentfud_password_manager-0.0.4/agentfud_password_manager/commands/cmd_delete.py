import click
from agentfud_password_manager.models import Entry, Session, Config
from agentfud_password_manager.utils import check_master_password
from rich import print as printc

@click.command()
@click.option('-i', '--id', help='Deletes a single entry by id', required=True)
@click.option("--master_password", prompt=True, hide_input=True)
def cli(id, master_password):
    """
    Deletes an entry
    """

    with Session() as session:
        config = session.query(Config).first()
        master_password_hash = config.master_password_hash
    
    if check_master_password(master_password, master_password_hash):
        printc(f"[green][+] Master password is ok. [/green]")
    else:
        raise click.Abort()
    with Session() as session:
        entry = session.query(Entry).filter(Entry.id == id).first()
        if entry is not None:
            session.delete(entry)
            session.commit()

    if entry is not None:
        printc(f"[green][+] Entry deleted successfully: [{id} {entry.site_url}]. [/green]")
    else:
        printc(f"[red][+] There is no entry with the id: [{id}]. [/red]") 
    