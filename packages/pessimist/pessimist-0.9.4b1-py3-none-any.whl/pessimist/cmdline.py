import logging
import sys

import click

from .manager import Manager


@click.command()
@click.option(
    "--extend", default="", help="Ignore all bounds on these comma-separated packages"
)
@click.option("--fast", is_flag=True, help="Only check extremes")
@click.option(
    "--command", "-c", default="make test", help="Command to run with PATH from venv"
)
@click.option("--verbose", "-v", is_flag=True, help="Show more logging")
@click.argument("target_dir")
def main(target_dir: str, extend: str, fast: bool, command: str, verbose: bool):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.WARNING)

    mgr = Manager(
        Path(target_dir).resolve(), command=command, extend=extend.split(","), fast=fast
    )
    if not mgr.solve():
        sys.exit(1)
