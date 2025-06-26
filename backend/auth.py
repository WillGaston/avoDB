import psycopg2
import os
import sys

from backend.dbInit import cursorCreation, cursorRemoval

def addUserToDB(userId, username, hashedPassword, kek_salt, pk_iv, encryptedPrivateKey, publicKey, createdTime):
  qry = "insert into UsersMeta(user_id, username, kek_salt, pk_iv, hashed_password, encrypted_private_key, public_key, created_at) values(%s, %s, %s, %s, %s, %s, %s, %s) returning user_id"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [userId, username, kek_salt, pk_iv, hashedPassword, encryptedPrivateKey, publicKey, createdTime])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('Registration Failed: ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    return False

  return True

def getHashedPassword(userId):
  qry = "select hashed_password from UsersMeta where user_id = %s"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [userId])
  result = cursor.fetchall()

  cursorRemoval(cursor, connection)
  # error checking
  return result[0][0]

def getUserData(userId):
  qry = "select encrypted_private_key, public_key, kek_salt, pk_iv from UsersMeta where user_id = %s"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [userId])
  result = cursor.fetchall()

  cursorRemoval(cursor, connection)
  # error checking
  return result[0]

def checkDBBelongsToUser(userId, dbId):
  qry = "select count(*) from Databases where owner_id = %s and db_id = %s"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [userId, dbId])
  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None or value[0] == 0:
    return False

  return True

def checkTBBelongsToUser(userId, tbId):
  qry = "select count(*) " \
  "from Tables t " \
  "join Databases d on d.db_id = t.db_id " \
  "join UsersMeta u on u.user_id = d.owner_id " \
  "where u.user_id = %s and t.table_id = %s;"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [userId, tbId])
  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None or value[0] == 0:
    return False

  return True

def checkRowBelongsToUser(userId, rowId):
  qry = "select count(*) " \
  "from Tables t " \
  "join Databases d on d.db_id = t.db_id " \
  "join UsersMeta u on u.user_id = d.owner_id " \
  "join Rows r on r.table_id = t.table_id " \
  "where u.user_id = %s and r.row_id = %s;"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [userId, rowId])
  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None or value[0] == 0:
    return False

  return True

def listUsers():
  qry = "select username, user_id from UsersMeta;"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [])
  value = cursor.fetchall()
  cursorRemoval(cursor, connection)
  
  if value is None:
    return False

  return value