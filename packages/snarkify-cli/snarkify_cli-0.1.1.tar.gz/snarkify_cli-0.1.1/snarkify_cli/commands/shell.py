import subprocess

import requests
from typing import Optional

import typer
from rich import print
from rich.table import Table

from snarkify_cli.lib.command import logged_in_command
from snarkify_cli.lib.configs import CliConfig
from snarkify_cli.lib.http_utils import (
    create_shell,
    delete_shell,
    # start_shell,
    # stop_shell,
    list_shells,
    get_shell,
    get_catalogs,
)
from snarkify_cli.lib.prompt_utils import CONSOLE
from snarkify_cli.lib.prompt_utils import prompt_for_selection, PROMPT_SELECTION_TYPE

shell_app = typer.Typer(no_args_is_help=True, help="Manages shells within Snarkify platform.")
SHELL_INFO_KEYS = [
    "shell_id",
    "shell_name",
    "team_name",
    "state",
    "created",
    "username",
    "hostname",
    "port",
]


@logged_in_command(shell_app)
def create(name: Optional[str] = typer.Argument(None, help="Shell name")) -> None:
    """
    Registers a new shell within Snarkify platform.
    If shell name is not set, it will be default to the shell id.

    Note that a shell can't be suspended/restarted and all data will be lost once it's shut down.
    """
    if CliConfig.team_id is None:
        print("Please select a team using `snarkify team switch`.")
        raise typer.Exit(code=1)
    try:
        catalogs = get_catalogs(CliConfig.team_id)
        shell_sku_prices = catalogs.get("shell")
        if not shell_sku_prices:
            print("Team not whitelisted for shell feature")
            raise typer.Exit(code=1)
        selected_catalog_idx = prompt_for_selection(
            [sku_price["sku"]["display_name"] for sku_price in shell_sku_prices], PROMPT_SELECTION_TYPE.CATALOG
        )
        selected_sku_price = shell_sku_prices[selected_catalog_idx]
        sku_display_name = shell_sku_prices[selected_catalog_idx]["sku"]["display_name"]
        print(f"You've successfully selected {sku_display_name} for your shell.")
        shell_id = create_shell(
            CliConfig.team_id, name, selected_sku_price["sku"]["sku_id"], selected_sku_price["unit_price"]["price_id"]
        )
        print(f"Your remote shell is being created, you can check if it's ready with `snarkify shell info {shell_id}`.")
    except Exception as ex:
        print(f"Failed to create shell due to {ex}.")


# Temporary disable start and stop shell commands because it would cause data loss in the shell.
# We need to re-enable it after the feature is stable.
# @logged_in_command(shell_app)
# def start(shell_id: str = typer.Argument(..., help="Shell id")) -> None:
#     """
#     Starts a shell.
#     """
#     try:
#         start_shell(shell_id)
#         print(f"Your remote shell {shell_id} will be started shortly.")
#     except Exception as ex:
#         print(f"Failed to start shell due to {ex}.")


# """
# @logged_in_command(shell_app)
# def stop(shell_id: str = typer.Argument(..., help="Shell id")) -> None:
#     """
#     Stops a shell.
#     """
#     try:
#         stop_shell(shell_id)
#         print(f"Your remote shell {shell_id} will be stopped shortly.")
#     except Exception as ex:
#         print(f"Failed to stop shell due to {ex}.")
# """


@logged_in_command(shell_app)
def delete(shell_id: str = typer.Argument(..., help="Shell id")) -> None:
    """
    Deletes a shell.

    Note that a shell can't be suspended/restarted and all data will be lost once it's shut down.
    """
    try:
        delete_shell(shell_id)
        print(f"Your remote shell {shell_id} will be deleted shortly.")
    except Exception as ex:
        print(f"Failed to delete shell due to {ex}.")


@logged_in_command(shell_app)
def info(shell_id: str = typer.Argument(..., help="Shell id")) -> None:
    """
    Retrieves shell information.
    """
    try:
        shell_info = get_shell(shell_id)
        table = Table(show_header=False, show_lines=True)
        for key in SHELL_INFO_KEYS:
            table.add_row(key.replace("_", " "), str(shell_info[key]))
        CONSOLE.print(table)
    except Exception as ex:
        print(f"Failed to retrieve shell due to {ex}.")


@logged_in_command(shell_app)
def connect(shell_id: str = typer.Argument(..., help="Shell id")) -> None:
    """
    Connect to a shell
    """
    try:
        shell_info = get_shell(shell_id)
        host_name = shell_info["hostname"]
        port = shell_info["port"]
        user_name = shell_info["username"]
        command = ["ssh", "-p", str(port), f"{user_name}@{host_name}"]
        subprocess.run(command, check=True)
    except Exception as ex:
        print(f"Failed to connect to shell {shell_id} due to {ex}.")


@logged_in_command(shell_app)
def list() -> None:
    """
    Lists all shells.

    Displays a list of all shells under current active team.
    """
    if CliConfig.team_id is None:
        print("Please select a team using `snarkify team switch`.")
        raise typer.Exit(code=1)
    try:
        shells = list_shells(CliConfig.team_id)
        if len(shells) == 0:
            print("No shells found.")
            return
        table = Table(show_header=False, show_lines=True)
        table.add_row("shell id", "shell name")
        for shell in shells:
            table.add_row(shell["shell_id"], shell["shell_name"])
        CONSOLE.print(table)
    except requests.HTTPError as ex:
        print(f"Fail to list shells due to {ex}")
        raise typer.Exit(code=1)
