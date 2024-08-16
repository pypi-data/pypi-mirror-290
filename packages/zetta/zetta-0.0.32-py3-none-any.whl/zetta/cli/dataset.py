# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

dataset_cli = typer.Typer(
    name="dataset",
    help="Manage your datasets in Zetta AI Network.",
    no_args_is_help=True,
)


@dataset_cli.command(name="create", help="create a new dataset repo.")
@synchronizer.create_blocking
async def create(json: bool = False):
    pass


@dataset_cli.command(name="delete", help="delete a dataset repo")
@synchronizer.create_blocking
async def delete(json: bool = False):
    pass


@dataset_cli.command(name="ownership", help="list dataset ownership.")
@synchronizer.create_blocking
async def ownership(json: bool = False):
    pass


@dataset_cli.command(
    name="lineage", help="list the lineage (with rewards info) for the dataset."
)
@synchronizer.create_blocking
async def lineage(json: bool = False):
    pass


@dataset_cli.command(name="logs", help="list the access logs for the dataset.")
@synchronizer.create_blocking
async def logs(json: bool = False):
    pass


@dataset_cli.command(name="history", help="list the git history for the dataset.")
@synchronizer.create_blocking
async def history(json: bool = False):
    pass


@dataset_cli.command(name="register", help="register dataset.")
@synchronizer.create_blocking
async def register(json: bool = False):
    pass
