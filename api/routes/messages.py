import base64
from tabulate import tabulate

from backend.messages import *
from backend.sharedOp import getUsername
from client.cryptography.encryption import decryptMessage, decryptWithPrivateKey, encryptMessage, encryptWithPublicKey
from client.cryptography.keyGeneration import generateIV, generateMasterKey, generateUserId
from client.storage.sessionManagement import getConvoUserID, getPassword, getPrivateKey, getPublicKey, getRecipientPublicKey, getUserID, initiateConvo

def initiateConvoRoute(userId):
  # 1. get user's public key
  # 2. add userid and public key to keyring
  print('blah')
  publicKey = getReceiverPublicKey(userId)
  initiateConvo(userId, publicKey)
  print('Successfully initiated conversation')

def viewConvosRoute():
  convos = viewConvos(getUserID())
  print(tabulate(convos, headers=['username', 'userId']))

def sendMsgRoute(message):
  senderId = getUserID()
  recipientId = getConvoUserID()
  recipientPublicKey = base64.b64decode(getRecipientPublicKey())
  senderPublicKey = getPublicKey()
  
  messageId = generateUserId()
  messageKey = generateMasterKey()
  iv = generateIV()

  encryptedMessage = encryptMessage(message, iv, messageKey)
  encryptedSenderKey = encryptWithPublicKey(messageKey, senderPublicKey)
  encryptedSenderKey = base64.b64encode(encryptedSenderKey).decode('utf-8')
  encryptedRecipientKey = encryptWithPublicKey(messageKey, recipientPublicKey)
  encryptedRecipientKey = base64.b64encode(encryptedRecipientKey).decode('utf-8')

  if sendMsg(messageId, encryptedMessage, senderId, recipientId, encryptedSenderKey, encryptedRecipientKey, iv):
    print('Message sent successfully')

def viewMsgsRoute():
  senderId = getUserID()
  recipientId = getConvoUserID()

  otherUser = getUsername(recipientId)

  encryptedUserSentMessages = viewMsgs(senderId, recipientId, True)

  userSentMessages = []
  
  for message in encryptedUserSentMessages:
    encryptedSenderKey = base64.b64decode(message[3])
    messageKey = decryptWithPrivateKey(getPrivateKey(), encryptedSenderKey, getPassword())
    decryptedMessage = decryptMessage(message[0], message[2], messageKey).decode('utf-8')
    sentAt = message[1]

    userSentMessages.append([decryptedMessage, sentAt])

  encryptedUserReceivedMessages = viewMsgs(recipientId, senderId, False)

  userReceivedMessages = []
  
  for message in encryptedUserReceivedMessages:
    encryptedSenderKey = base64.b64decode(message[3])
    messageKey = decryptWithPrivateKey(getPrivateKey(), encryptedSenderKey, getPassword())
    decryptedMessage = decryptMessage(message[0], message[2], messageKey).decode('utf-8')
    sentAt = message[1]

    userReceivedMessages.append([decryptedMessage, sentAt])

  taggedMessagesCurr = [('curr', timestamp, message) for message, timestamp in userSentMessages]
  taggedMessagesOther = [('other', timestamp, message) for message, timestamp in userReceivedMessages]

  combinedMessages = taggedMessagesCurr + taggedMessagesOther
  combinedMessages.sort(key=lambda x: x[1])

  rows = []
  for sender, timestamp, message in combinedMessages:
    if sender == 'curr':
      rows.append(["", message])
    else:
      rows.append([message, ""])

  print(tabulate(rows, headers=[f'{otherUser}', 'Me']))