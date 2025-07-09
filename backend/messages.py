from backend.dbInit import cursorCreation, cursorRemoval

def viewConvos(currUserId):
  qry = "select distinct u.username, u.user_id " \
  "from Messages m " \
  "join UsersMeta u ON ( " \
  "(m.receiver_id = u.user_id AND m.sender_id = %s) OR "\
  "(m.sender_id = u.user_id AND m.receiver_id = %s));"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [currUserId, currUserId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('Registration Failed: ', e)

  value = cursor.fetchall()
  cursorRemoval(cursor, connection)
  
  if value is None:
    return False

  return value

def sendMsg(messageId, encryptedMsg, senderId, recipientId, encryptedSenderKey, encryptedReceiverKey, iv):
  qry = "insert into Messages(message_id, encrypted_message, sender_id, receiver_id, encrypted_sender_key, encrypted_receiver_key, iv) values (%s, %s, %s, %s, %s, %s, %s) returning message_id"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [messageId, encryptedMsg, senderId, recipientId, encryptedSenderKey, encryptedReceiverKey, iv])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('message failed to sent: ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    return False

  return True

def viewMsgs(senderId, recipientId, isSender):
  if isSender:
    qry = "select encrypted_message, sent_at, iv, encrypted_sender_key " \
    "from Messages " \
    "where sender_id = %s and receiver_id = %s;"
  else:
    qry = "select encrypted_message, sent_at, iv, encrypted_receiver_key " \
    "from Messages " \
    "where sender_id = %s and receiver_id = %s;"
  
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [senderId, recipientId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('Cannot view messages: ', e)

  value = cursor.fetchall()
  cursorRemoval(cursor, connection)
  
  if value is None:
    return False

  return value

""" def getConvoKeys(senderId, recipientId):

  qry = "select encrypted_sender_key " \
  "from Messages " \
  "where sender_id = %s and receiver_id = %s" \
  "union " \
  "select encrypted_receiver_key " \
  "from Messages " \
  "where receiver_id = %s and sender_id = %s;"
  
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [senderId, recipientId, senderId, recipientId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('no conversation between these users: ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    return False

  return value[0] """

def getReceiverPublicKey(receiverId):
  qry = "select public_key " \
  "from UsersMeta " \
  "where user_id = %s;"
  cursor, connection = cursorCreation()

  try:
    cursor.execute(qry, [receiverId])
    connection.commit()
  except Exception as e:
    connection.rollback()
    print('could not get public key: ', e)

  value = cursor.fetchone()
  cursorRemoval(cursor, connection)
  
  if value is None:
    return False

  return value[0]