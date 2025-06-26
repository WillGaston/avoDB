import psycopg2
import os
import sys

from backend.dbInit import cursorCreation, cursorRemoval

def addTable(tableId, dbId, tbName, schema):
  qry = "insert into Tables(table_id, db_id, encrypted_table_name, encrypted_schema) values(%s, %s, %s, %s) returning db_id"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [tableId, dbId, tbName, schema])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('Table Creation Failed: ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    print('failed to add table')
    sys.exit(1)

  print('Successfully added table')
  return True

def listTables(dbId):
  qry = "select table_id, encrypted_table_name, encrypted_schema from Tables where db_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [dbId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('list Tables failed: ', e)

  value = cursor.fetchall()
  cursorRemoval(cursor, connection)

  if value is None:
    print('list failed')
    sys.exit(1)

  return value

def deleteTable(dbId, tbId):
  qry = "delete from Tables where db_id = %s and table_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [dbId, tbId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('deletion failed:', e)

  cursorRemoval(cursor, connection)

  print('Successfully deleted table')
  return True

def getSchema(tbId, dbId):
  qry = "select encrypted_schema from Tables where db_id = %s and table_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [dbId, tbId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('list schema failed: ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    print('schema failed')
    sys.exit(1)

  return value[0]
 
def getTableName(dbId, tbId):
  qry = "select encrypted_table_name from Tables where db_id = %s and table_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [dbId, tbId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('couldn\'t retrieve table name ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    print('name retrieval failed')
    sys.exit(1)

  return value[0]