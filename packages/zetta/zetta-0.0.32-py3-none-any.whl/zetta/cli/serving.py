# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

serving_cli = typer.Typer(
    name="serving",
    help="Manage your inference serving in Zetta AI Network.",
    no_args_is_help=True,
)


@serving_cli.command(
    name="list",
    help="List all the visible inference endpoints that are currently running.",
)
@synchronizer.create_blocking
async def list(model: str = "all"):
    # machine type, replica and remain-time will show here
    pass


@serving_cli.command(
    name="status", help="Show the stats information of the inference endpoints."
)
@synchronizer.create_blocking
async def stats(endpoint: str = "all"):
    # machine type, replica and remain-time will show here
    pass


@serving_cli.command(name="deploy", help="Deploy a model for serving.")
@synchronizer.create_blocking
async def deploy(
    model: str = "", machine_type: str = "", duration: str = "", replica: int = 1
):
    pass


@serving_cli.command(name="renew", help="Renew a model for serving.")
@synchronizer.create_blocking
async def renew(model: str = "", duration: str = ""):
    pass


@serving_cli.command(name="update", help="Update a serving config")
@synchronizer.create_blocking
async def update(config: str):
    # machine type, replica and remain-time can be change here
    pass


@serving_cli.command(name="shell", help="Open a shell to chat with model")
@synchronizer.create_blocking
async def shell(model: str = "", endpoint: str = "any"):
    pass


@serving_cli.command(
    name="batch",
    help="Execuate batch inference for model, default delimiter is newline ",
)
@synchronizer.create_blocking
async def batch(
    model: str = "", endpoint: str = "any", inputs: str = "", delimiter: str = ""
):
    pass
