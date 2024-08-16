import click
from agentfud_password_manager.models import Entry, Config, Session
from agentfud_password_manager.utils import decrypt, get_master_key, check_master_password
from rich import print as printc
import pyperclip


@click.command()
@click.option('-i', '--id', help='Searches for a single password and returns it', required=True)
@click.option("--master_password", prompt=True, hide_input=True)
def cli(id, master_password):
    """
    Decrypts the password and copies it to the clipboard
    """
    with Session() as session:
        config = session.query(Config).first()
        master_password_hash = config.master_password_hash
        device_salt = config.device_salt

        if check_master_password(master_password, master_password_hash):
            printc(f"[green][+] Master password is ok. [/green]")
        else:
            raise click.Abort()
    
    master_key = get_master_key(master_password, device_salt)

    with Session() as session:
        entry = session.query(Entry).filter(Entry.id == id).first()
        if entry is not None:
            decrypted_password = decrypt(entry.password, master_key)
            pyperclip.copy(decrypted_password)

    if entry is not None:
        printc(f"[green][+] Entry retrieved successfully: [{id} / {entry.site_url}]. [/green]")
    else:
        printc(f"[red][+] There is no entry with the id: [{id}]. [/red]")            