import click
from agentfud_password_manager.models import Entry, Config, Session
from rich import print as printc
from agentfud_password_manager.utils import generate_password, encrypt, check_master_password, get_master_key


@click.command()
@click.option('-su', '--site-url', help='URL of the site where you want to log in')
@click.option('-u', '--username', help='User name')
@click.option('-e', '--email', help='Email address')
@click.option('-p', '--password', help='Password')
@click.option("--master_password", prompt=True, hide_input=True)
def cli(site_url, username, email, password, master_password):
    """
    Adding a new entry to the database
    """
    with Session() as session:
        config = session.query(Config).first()
        master_password_hash = config.master_password_hash
        device_salt = config.device_salt
    
    if check_master_password(master_password, master_password_hash):
        printc(f"[green][+] Master password is ok. [/green]")
    else:
        raise click.Abort()

        # If no password provided we'll generate a secure one
    if password is None:
        password = generate_password()
        printc(f"[green][+] New random password is generated. [/green]")

    master_key = get_master_key(master_password, device_salt)

    new_entry = Entry(
        site_url = site_url,
        username = username,
        email = email,
        password = encrypt(password, master_key)
    )

    with Session() as session:
        session.add(new_entry)
        session.commit()

    printc(f"[green][+] New entry added successfully: {site_url}. [/green]")