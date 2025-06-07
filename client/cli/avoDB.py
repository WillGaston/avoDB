import click
from auth import *
from tables import *

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

if __name__ == '__main__':
  avoDB_CLI()