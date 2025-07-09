import sys

from backend.dbInit import cursorCreation, cursorRemoval

def addDB(dbId, ownerId, iv, encryptedDBName, encryptedMasterKey):
  qry = "insert into Databases(db_id, owner_id, iv, encrypted_db_name, encrypted_master_key) values(%s, %s, %s, %s, %s) returning owner_id"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [dbId, ownerId, iv, encryptedDBName, encryptedMasterKey])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('Database Insertion Failed: ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    print('failed to add db')
    sys.exit(1)

  print('Successfully added database')
  return True

def listDBs(ownerId):
  qry = "select db_id, encrypted_db_name, encrypted_master_key from Databases where owner_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [ownerId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('list DB failed: ', e)

  value = cursor.fetchall()
  cursorRemoval(cursor, connection)
  
  if value is None:
    print('list failed')
    sys.exit(1)

  return value

def deleteDB(ownerId, dbId):
  qry = "delete from Databases where owner_id = %s and db_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [ownerId, dbId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('deletion failed:', e)

  cursorRemoval(cursor, connection)

  print('Successfully deleted db')
  return True

def getMasterKey(dbId):
  qry = "select encrypted_master_key from Databases where db_id = %s"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [dbId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('failed to get db master key: ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    print('list failed')
    sys.exit(1)

  return value[0]