import click

from viavi.fibermark.db_utils.ping_db import ping_ip
from viavi.fibermark.db_utils.settings import DB_URI

if not ping_ip(DB_URI):
    raise RuntimeError("Package needs to be able to connect to DB, please verify your network")

from viavi.fibermark.cli_commands.add import add
from viavi.fibermark.cli_commands.compare import compare
from viavi.fibermark.cli_commands.note import note
from viavi.fibermark.cli_commands.remote import remote
from viavi.fibermark.cli_commands.show import show
from viavi.fibermark.cli_commands.update import update


@click.group()
def cli():
    """Curve Measure Notation CLI"""


def run():
    cli.add_command(add)
    cli.add_command(compare)
    cli.add_command(note)
    cli.add_command(show)
    cli.add_command(remote)
    cli.add_command(update)
    cli()


if __name__ == "__main__":
    run()
