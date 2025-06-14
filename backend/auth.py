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
  qry = "select hashed_password from Users where userId = %s"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [userId])
  result = cursor.fetchall()

  cursorRemoval(cursor, connection)
  # error checking
  return result[0]

