import click
from rich import print as printc
import hashlib
import random
import string
from agentfud_password_manager.models import Base, db, Config, Session

@click.command()
@click.option("--password", hide_input=True, confirmation_prompt=True, prompt='Your Master Password')
def cli(password):
    """
    Initialization of the password manager
    """
    Base.metadata.create_all(db)
    printc("[green][+] Tables created. [/green]")

    hashed_master_password = hashlib.sha256(password.encode()).hexdigest()
    
    device_salt = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=32))

    config = Config(master_password_hash=hashed_master_password, device_salt=device_salt)

    with Session() as session:
        session.add(config)
        session.commit()
    
    printc("[green][+] Application configured properly. [/green]")