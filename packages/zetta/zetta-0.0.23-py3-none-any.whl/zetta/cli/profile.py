# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

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
async def list(json: bool = False):
    pass


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
    pass
