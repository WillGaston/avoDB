import click
from client.cli.auth import *
from client.cli.tables import *

avoDB_banner = r"""
avoDB: an end-to-end encrypted database as a service.
"""

@click.group(help=avoDB_banner)
def avoDB_CLI():
  pass

avoDB_CLI.add_command(auth)
avoDB_CLI.add_command(db)
avoDB_CLI.add_command(tb)
avoDB_CLI.add_command(rw)