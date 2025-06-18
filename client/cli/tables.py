import click

from api.routes.tables import *

#----------------------------------------------#
#           Database Commands                  #
#----------------------------------------------#

@click.group()
def db():
  pass

@click.command(help="--name <*name*>")
@click.option('--name', prompt=True, help="name of database being created")
def dbCreate(name):
  createDB(name)

@click.command(help="")
def dbList():
  listDB()

@click.command(help="--dbId <*dbId*>")
@click.option('--dbID', prompt=True, help="id of the database being deleted")
def dbDelete(dbId):
  print('blah')
  print(dbId)

db.add_command(dbCreate)
db.add_command(dbList)
db.add_command(dbDelete)

#----------------------------------------------#
#           Table Commands                     #
#----------------------------------------------#

@click.group()
def tb():
  pass

@click.command(help="--dbId <*dbId*> --name <*name*> --schema <*schema*>")
@click.option('--dbId', prompt=True, help="id of database table will belong to")
@click.option('--name', prompt=True, help="name of table being created")
@click.option('--schema', prompt=True, help="name of table being created")
def tbCreate(dbId, name, schema):
  print('blah')
  print(dbId)
  print(name)
  print(schema)

@click.command(help="--dbId <*dbId*>")
@click.option('--dbId', prompt=True, help="id of database")
def tbList(dbId):
  print('blah')
  print(dbId)

@click.command(help="--dbId <*dbId*> --tbId <*tbId*>")
@click.option('--dbId', prompt=True, help="id of database")
@click.option('--tbId', prompt=True, help="id of table")
def tbSchema(dbId, tbId):
  print('blah')
  print(dbId)
  print(tbId)

@click.command(help="--dbId <*dbId*> --tbId <*tbId*> ")
@click.option('--dbId', prompt=True, help="id of database")
@click.option('--tbId', prompt=True, help="id of table")
def tbDelete(dbId, tbId):
  print('blah')
  print(dbId)
  print(tbId)

tb.add_command(tbCreate)
tb.add_command(tbList)
tb.add_command(tbSchema)
tb.add_command(tbDelete)

#----------------------------------------------#
#           data/row Commands                  #
#----------------------------------------------#

@click.group()
def rw():
  pass

@click.command(help="--dbId <*dbId*> --tbId <*tbId*> --data <*data*>")
@click.option('--dbId', prompt=True, help="id of database")
@click.option('--tbId', prompt=True, help="id of table")
@click.option('--data', prompt=True, help="data to be inserted")
def insert(dbId, tbId, data):
  print('blah')
  print(dbId)
  print(tbId)
  print(data)

@click.command(help="--dbId <*dbId*> --tbId <*tbId*>")
@click.option('--dbId', prompt=True, help="id of database")
@click.option('--tbId', prompt=True, help="id of table")
def select(dbId, tbId):
  print('blah')
  print(dbId)
  print(tbId)

@click.command(help="--dbId <*dbId*> --tbId <*tbId*> --rwId <*rwId*>")
@click.option('--dbId', prompt=True, help="id of database")
@click.option('--tbId', prompt=True, help="id of table")
@click.option('--rwId', prompt=True, help="id of row to be deleted")
def rwDelete(dbId, tbId, rwId):
  print('blah')
  print(dbId)
  print(tbId)
  print(rwId)

rw.add_command(insert)
rw.add_command(select)
rw.add_command(rwDelete)