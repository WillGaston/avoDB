import psycopg2
import psycopg2.pool
import os
import sys
from dotenv import load_dotenv

load_dotenv()
dbPool = None

# create a collection of database connections for later use
def initDBPool():
  try:
    global dbPool
    dbPool = psycopg2.pool.SimpleConnectionPool(
      1, # min connections
      10, # max connections
      dbname=os.environ["POSTGRES_DB"],
      user=os.environ["POSTGRES_USER"],
      password=os.environ["POSTGRES_PASSWORD"],
      host=os.environ.get("POSTGRES_HOST", "localhost"),
      port=os.environ.get("POSTGRES_PORT", 5432),
    )
  except Exception as e:
    print(f'DB pool error: {e}')
    sys.exit(1)

# gets a db connection from the pool
def getConnection():
  # exception handling
  return dbPool.getconn()

# relinqueshes a db connection back to the pool
def releaseConnection(connection):
  # error handling
  dbPool.putconn(connection)

# close all connections in the db pool
def closeDBPool():
  dbPool.closeall()

# boilerplater for creating a cursor
def cursorCreation():
  cursor = None
  connection = None
  try:
    connection = getConnection()
    cursor = connection.cursor()
  except Exception:
    print('cursor creation failed')
    print(Exception)

  return cursor, connection

# boilerplate for closing a cursor
def cursorRemoval(cursor, connection):
  cursor.close()
  releaseConnection(connection)
