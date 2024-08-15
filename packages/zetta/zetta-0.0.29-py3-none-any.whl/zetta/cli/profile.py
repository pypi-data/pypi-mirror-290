# Copyright ZettaBlock Labs 2024
import typer
import os
import configparser
import pyfiglet
import requests
from colorama import Fore, Style, init
from zetta._utils.async_utils import synchronizer

SERVICE_GET_USER_URL = "https://neo-dev.prod.zettablock.com/v1/api/user"
init(autoreset=True)

profile_cli = typer.Typer(
    name="profile",
    help="Manage your profile, only 1 profile could be active in Zetta AI Network.",
    no_args_is_help=True,
)


@profile_cli.command(name="logout", help="logout the current user")
@synchronizer.create_blocking
async def logout(json: bool = False):
    pass


@profile_cli.command(
    name="list", help="List all tokens and wallet for the current profile"
)
@synchronizer.create_blocking
async def list():
    zetta_root = os.getenv("ZETTA_ROOT")
    if not zetta_root:
        raise EnvironmentError("ZETTA_ROOT env variable is not set.")
    secrets_path = os.path.join(zetta_root, ".zetta/secrets")
    try:
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
        headers = {
            "Authorization": token
        }
        response = requests.get(SERVICE_GET_USER_URL, headers=headers)
        if response.status_code == 200:
            data = response.json()
            tokens = data['data']['profile']['tokens']
            wallet_address = data['data']['profile']['wallet_address']
            api_key = data['data']['profile']['api_key']
            block_text = pyfiglet.figlet_format("ZETTA", font="block")
            block_text = block_text.rstrip()
            print(f"{block_text}\n")
            print(f"{Fore.BLUE}[Tokens]{Style.RESET_ALL}")
            for token in tokens:
                token_output = f"{token['name']} {token['id']}"
                if token['is_default']:
                    token_output += f"{Fore.GREEN} <- default{Style.RESET_ALL}"
                print(token_output)
            print(f"{Fore.BLUE}[Wallet Address]{Style.RESET_ALL}")
            print(wallet_address)
            print(f"{Fore.BLUE}[API Keys]{Style.RESET_ALL}")
            print(api_key)
        else:
            response.raise_for_status()
    except FileNotFoundError:
        print(f"File not found: {secrets_path}")
    except IOError:
        print(f"An error occurred while reading the file: {secrets_path}")
    pass


def print_boxed_text(text):
    lines = text.splitlines()
    max_length = max(len(line) for line in lines)
    print("┌" + "─" * (max_length + 2) + "┐")
    for line in lines:
        print(f"│ {line.ljust(max_length)} │")
    print("└" + "─" * (max_length + 2) + "┘")


@profile_cli.command(name="token-add", help="Add a token for the current profile")
@synchronizer.create_blocking
async def add_token(json: bool = False):
    pass


@profile_cli.command(name="token-remove", help="remove a token for the current profile")
@synchronizer.create_blocking
async def remove_token(json: bool = False):
    pass


@profile_cli.command(name="info", help="The current profile info")
@synchronizer.create_blocking
async def info(json: bool = False):
    zetta_root = os.getenv("ZETTA_ROOT")
    if not zetta_root:
        raise EnvironmentError("ZETTA_ROOT env variable is not set.")
    profile_path = os.path.join(zetta_root, ".zetta/profile")
    try:
        # Open the file in read mode ('r')
        with open(profile_path, 'r') as file:
            content = file.read()
            print(content,end="")
    except FileNotFoundError:
        print(f"File not found: {profile_path}")
    except IOError:
        print(f"An error occurred while reading the file: {profile_path}")
    pass
