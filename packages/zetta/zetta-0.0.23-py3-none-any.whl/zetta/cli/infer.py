# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

infer_cli = typer.Typer(
    name="infer",
    help="Send inference requests to Zetta AI network.",
    no_args_is_help=True,
)


@infer_cli.command(
    name="list",
    help="List all the visible inference endpoints for a network.",
)
@synchronizer.create_blocking
async def list(model: str = "all"):
    # machine type, replica and remain-time will show here
    pass


@infer_cli.command(
    name="status", help="Show the stats information of the inference endpoints."
)
@synchronizer.create_blocking
async def status(endpoint: str = "all"):
    # machine type, replica and remain-time will show here
    pass


@infer_cli.command(name="shell", help="Open a shell to chat with model")
@synchronizer.create_blocking
async def shell(model: str = "", endpoint: str = "any"):
    pass


@infer_cli.command(name="chat", help=" chat with model")
@synchronizer.create_blocking
async def chat(model: str = "", endpoint: str = "any"):
    pass


@infer_cli.command(
    name="history",
    help="Check the inference history. ",
)
@synchronizer.create_blocking
async def history(
    model: str = "", endpoint: str = "any", inputs: str = "", delimiter: str = ""
):
    pass
