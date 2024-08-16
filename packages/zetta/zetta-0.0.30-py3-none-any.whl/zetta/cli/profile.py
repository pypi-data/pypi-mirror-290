# Copyright ZettaBlock Labs 2024
import typer
import os
import configparser
import requests
from termcolor import colored
from zetta._utils.async_utils import synchronizer

SERVICE_GET_USER_URL = "https://neo-dev.prod.zettablock.com/v1/api/user"
SERVICE_TOKEN_URL = "https://neo-dev.prod.zettablock.com/v1/api/user/token"

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
    try:
        zetta_root = os.getenv("ZETTA_ROOT")
        if not zetta_root:
            raise EnvironmentError("ZETTA_ROOT env variable is not set.")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
        headers = {
            "Authorization": token
        }
        response = requests.get(SERVICE_GET_USER_URL, headers=headers)
        data = response.json()
        if response.status_code == 200:
            print_array_info(data['data']['profile']['tokens'], "tokens")
            print_info(data['data']['profile']['api_key'], "api keys")
            print_info(data['data']['profile']['wallet_address'], "wallet addresses")
        else:
            response.raise_for_status()
    except Exception as err:
        print(f"An unexpected error occurred: {data['error']}")
    pass


def print_info(info, text_title):
    title = colored(text_title, "blue")
    box_width = max(70, len(text_title)+2)
    print(f"┌{'─' * 4} {title} {'─' * (box_width - len(text_title) - 8)}┐")
    print(f"│ {info}{' ' * (box_width-len(info)-4)} │")
    print(f"└{'─' * (box_width - 2)}┘")


def print_array_info(tokens, text_title):
    title = colored(text_title, "blue")
    token_line_length = 0
    for token in tokens:
        l = len(f"{token['name']} {token['id']}")
        if token['is_default']:
            l += 11
        token_line_length = max(l, token_line_length)
    box_width = max(70, token_line_length+4)
    print(f"┌{'─' * 4} {title} {'─' * (box_width - len(text_title) - 8)}┐")
    for token in tokens:
        name = token['name']
        id = token['id']
        token_name = colored(name, "yellow")
        token_info = f"{token_name} {id}"
        l = len(name) + len(id) + 1
        if token['is_default']:
            token_info += colored(" <- default", "green")
            l += 11
        print(f"│ {token_info}{' ' * (box_width-l-4)} │")
    print(f"└{'─' * (box_width - 2)}┘")


@profile_cli.command(name="token-add", help="Add a token for the current profile")
@synchronizer.create_blocking
async def add_token(
    name: str = "",
    is_default: bool = False,
):
    try:
        zetta_root = os.getenv("ZETTA_ROOT")
        if not zetta_root:
            raise EnvironmentError("ZETTA_ROOT env variable is not set.")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
        headers = {
            "Authorization": token
        }
        body = {
            "name": name,
            "is_default": is_default
        }
        response = requests.post(SERVICE_TOKEN_URL, headers=headers, json=body)
        data = response.json()
        if response.status_code == 200:
            print("token added")
            print(data["data"])
        else:
            response.raise_for_status()
    except Exception as err:
        print(f"An unexpected error occurred: {data['error']}")
    pass


@profile_cli.command(name="token-remove", help="remove a token for the current profile")
@synchronizer.create_blocking
async def remove_token(token_id: str):
    try:
        zetta_root = os.getenv("ZETTA_ROOT")
        if not zetta_root:
            raise EnvironmentError("ZETTA_ROOT env variable is not set.")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
        headers = {
            "Authorization": token
        }
        url = f"{SERVICE_TOKEN_URL}?id={token_id}"
        response = requests.delete(url, headers=headers)
        data = response.json()
        if response.status_code == 200:
            print("token removed")
        else:
            response.raise_for_status()
    except Exception as err:
        print(f"An unexpected error occurred: {data['error']}")
        pass


@profile_cli.command(name="info", help="The current profile info")
@synchronizer.create_blocking
async def info(json: bool = False):
    try:
        zetta_root = os.getenv("ZETTA_ROOT")
        if not zetta_root:
            raise EnvironmentError("ZETTA_ROOT env variable is not set.")
        profile_path = os.path.join(zetta_root, ".zetta/profile")
        with open(profile_path, 'r') as file:
            content = file.read()
            print(content,end="")
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
    pass
