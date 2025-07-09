from backend.dbInit import cursorCreation, cursorRemoval

def checkUsernameExits(username):
  exists = False

  qry = "select count(distinct user_id) from usersmeta where username = %s"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [username])
  result = cursor.fetchone()

  if result is None:
    exists = False

  if result[0] > 0:
    exists = True

  cursorRemoval(cursor, connection)
  return exists

def getUserId(username):
  qry = "select user_id from UsersMeta where username = %s"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [username])
  result = cursor.fetchone()
  cursorRemoval(cursor, connection)
  # error checking
  return result[0]

def getUsername(userId):
  qry = "select username from UsersMeta where user_id = %s"
  cursor, connection = cursorCreation()

  cursor.execute(qry, [userId])
  result = cursor.fetchone()
  cursorRemoval(cursor, connection)
  # error checking
  return result[0]