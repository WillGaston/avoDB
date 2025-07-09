import keyring
import sys
from keyrings.alt.file import PlaintextKeyring

servicePrK = "avoDB_privateKey"
servicePbK = "avoDB_publicKey"
serviceP = "avoDB_password"
serviceU = "avoDB_userID"
serviceIV = "avoDB_iv"
convoUserId = "avoDB_convo_userID"
convoPublicKey = "avoDB_convo_publicKey"

username = "avoDB_username"
keyring.set_keyring(PlaintextKeyring()) # not secure, just for development/testing

def setCredentials(userId, privateKey, publicKey, password, iv):
  keyring.set_password(servicePrK, username, privateKey.decode())
  keyring.set_password(servicePbK, username, publicKey.decode())
  keyring.set_password(serviceP, username, password)
  keyring.set_password(serviceU, username, userId)
  keyring.set_password(serviceIV, username, iv)
  print('Successfully added credentials to keyring')

def initiateConvo(userId, publicKey):
  keyring.set_password(convoUserId, username, userId)
  keyring.set_password(convoPublicKey, username, publicKey)

def getPrivateKey():
  secret = keyring.get_password(servicePrK, username)
  if secret is None:
    print("not logged in, please log in first")
    sys.exit(1)

  return secret.encode()

def getPublicKey():
  secret = keyring.get_password(servicePbK, username)
  if secret is None:
    print("not logged in, please log in first")
    sys.exit(1)

  return secret.encode()

def getPassword():
  secret = keyring.get_password(serviceP, username)
  if secret is None:
    print("not logged in, please log in first")
    sys.exit(1)

  return secret.encode()

def getIV():
  secret = keyring.get_password(serviceIV, username)
  if secret is None:
    print("not logged in, please log in first")
    sys.exit(1)

  return secret

def getUserID():
  secret = keyring.get_password(serviceU, username)
  if secret is None:
    print("not logged in, please log in first")
    sys.exit(1)

  return secret

def getConvoUserID():
  secret = keyring.get_password(convoUserId, username)
  if secret is None:
    print("no conversation intitialised")
    sys.exit(1)

  return secret

def getRecipientPublicKey():
  secret = keyring.get_password(convoPublicKey, username)
  if secret is None:
    print("no conversation intitialised")
    sys.exit(1)

  return secret

def checkIfLoggedIn():
  secret = keyring.get_password(serviceP, username)
  if secret is not None:
    print('Already logged in')
    sys.exit(1)

def removeCredentials():
  if keyring.get_password(serviceP, username) is None:
    print('Not Currently Logged In')
    sys.exit(1)
  keyring.delete_password(servicePrK, username)
  keyring.delete_password(servicePbK, username)
  keyring.delete_password(serviceP, username)
  keyring.delete_password(serviceU, username)
  keyring.delete_password(serviceIV, username)
  if keyring.get_password(convoUserId, username) is not None:
    keyring.delete_password(convoUserId, username)
    keyring.delete_password(convoPublicKey, username)
    