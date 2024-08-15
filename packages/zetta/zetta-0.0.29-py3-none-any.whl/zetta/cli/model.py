# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

model_cli = typer.Typer(
    name="model",
    help="Manage your models in Zetta AI Network.",
    no_args_is_help=True,
)


@model_cli.command(name="create", help="create a new model repo.")
@synchronizer.create_blocking
async def create(json: bool = False):
    pass


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
