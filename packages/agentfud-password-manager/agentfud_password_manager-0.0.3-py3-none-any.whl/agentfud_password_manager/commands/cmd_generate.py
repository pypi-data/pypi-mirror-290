import click
from agentfud_password_manager.utils import generate_password
from rich import print as printc
import pyperclip

@click.command()
@click.option('--copy', is_flag=True, help='Copy new password to clipboard')
def cli(copy):
    """
    Generates a random password
    """
    new_password = generate_password()
    if copy:
        pyperclip.copy(new_password)
    else:
        printc(f"[blue][+] A new random password: {new_password}. [/blue]")