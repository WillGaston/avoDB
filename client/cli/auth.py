import click

from api.routes.auth import *

@click.group()
def auth():
  pass

@click.command(help="--username <*username*> --password <*password*>")
@click.option('--username', prompt=True, help="your username")
@click.option('--password', prompt=True, hide_input=True, help="your password")
def login(username, password):
  #loginFunc(username, password)
  print('blah')

@click.command(help="--username <*username*> --password <*password*>")
@click.option('--username', prompt=True, help="your username")
@click.option('--password', prompt=True, hide_input=True, help="your password")
def register(username, password):
  print('blah')
  print(username)
  print(password)
  registerFunc(username, password)

@click.command(help="")
def logout():
  print('blah')

auth.add_command(login)
auth.add_command(register)
auth.add_command(logout)