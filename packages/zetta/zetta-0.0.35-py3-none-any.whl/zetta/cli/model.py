# Copyright ZettaBlock Labs 2024
import configparser
import os
import requests
import typer
from zetta._utils.async_utils import synchronizer

model_cli = typer.Typer(
    name="model",
    help="Manage your models in Zetta AI Network.",
    no_args_is_help=True,
)

SERVICE_CREATE_MODEL_URL = "https://neo-dev.prod.zettablock.com/v1/api/asset"

@model_cli.command(name="create", help="create a new model repo.")
@synchronizer.create_blocking
async def create(model_name: str = typer.Argument(..., help="Name of the model"),
                    description: str = typer.Argument(..., help="Description of the model"),
                    license_type: str = typer.Argument(..., help="License type of the model"),
                    modality_type: str = typer.Argument(..., help="Modality of the model. E.g text, image, etc"),
                    private: bool = typer.Argument(..., help="Is the model private or not")):
    zetta_root = os.getenv("ZETTA_ROOT")

    if not zetta_root:
        raise EnvironmentError("ZETTA_ROOT env variable is not set.")
    secrets_path = os.path.join(zetta_root, ".zetta/secrets")

    try:
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
    except FileNotFoundError:
        print(f"File not found: {secrets_path}")
    except IOError:
        print(f"An error occurred while reading the file: {secrets_path}")

    headers = {
        "Authorization": token
    }

    json_data = {
        "type": "Model",
        "name": model_name,
        "license": license_type,
        "description": description,
        "private": private,
        "modality": modality_type
    }

    response = requests.post(SERVICE_CREATE_MODEL_URL, headers=headers, json=json_data)
    if response.status_code == 200:
        print(f'Successfully created model {model_name}')
    else:
        response.raise_for_status()


@model_cli.command(name="delete", help="delete a model repo")
@synchronizer.create_blocking
async def delete(json: bool = False):
    pass


@model_cli.command(name="ownership", help="list model ownership.")
@synchronizer.create_blocking
async def ownership(json: bool = False):
    pass


@model_cli.command(
    name="lineage", help="list the lineage (with rewards info) for the model."
)
@synchronizer.create_blocking
async def lineage(json: bool = False):
    pass


@model_cli.command(name="logs", help="list the access logs for the model.")
@synchronizer.create_blocking
async def logs(json: bool = False):
    pass


@model_cli.command(name="history", help="list the git history for the model.")
@synchronizer.create_blocking
async def history(json: bool = False):
    pass


@model_cli.command(name="register", help="register model.")
@synchronizer.create_blocking
async def register(json: bool = False):
    pass
