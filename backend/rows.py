import psycopg2
import os
import sys

from backend.dbInit import cursorCreation, cursorRemoval

def insertRow(rowId, tbId, encryptedData, iv):
  qry = "insert into Rows(row_id, table_id, encrypted_data, iv) values(%s, %s, %s, %s) returning row_id"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [rowId, tbId, encryptedData, iv])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('Row Insertion Failed: ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    print('failed to insert row')
    sys.exit(1)

  print('Successfully added row')
  return True

def selectRows(tbId):
  qry = "select encrypted_data, iv from Rows where table_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [tbId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('select Rows failed: ', e)

  value = cursor.fetchall()
  cursorRemoval(cursor, connection)
  
  if value is None:
    print('select failed')
    sys.exit(1)

  return value

def listRows(tbId):
  qry = "select encrypted_data, iv, row_id from Rows where table_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [tbId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('select Rows failed: ', e)

  value = cursor.fetchall()
  cursorRemoval(cursor, connection)
  
  if value is None:
    print('select failed')
    sys.exit(1)

  return value

def deleteRow(tbId, rwId):
  qry = "delete from Rows where table_id = %s and row_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [tbId, rwId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('row deletion failed:', e)

  cursorRemoval(cursor, connection)

  print('Successfully deleted row')
  return True