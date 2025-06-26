import datetime

from tabulate import tabulate

from backend.auth import *
from backend.sharedOp import checkUsernameExits, getUserId
from client.cryptography.encryption import *
from client.cryptography.keyGeneration import *
from client.cryptography.hashing import *
from client.storage.sessionManagement import *

def loginFunc(username, password):
  # 1. query db to check if username exists
  # 2. return the hashed password from the db
  # 3. verify hashed password
  # 4. save keys for session

  checkIfLoggedIn()

  userNameExists = checkUsernameExits(username)
  if not userNameExists:
    print('Username does not exist')
    return

  userId = getUserId(username)
  hashedPassword = getHashedPassword(userId)
  if not verifyPassword(hashedPassword, password):
    print('Incorrect password given')
    return
  
  # get private key
  encryptedPrivateKey, publicKey, salt, iv = getUserData(userId)
  encryptedPrivateKey = base64.b64decode(encryptedPrivateKey)
  publicKey = base64.b64decode(publicKey)
  #deserializedPrivateKey = deserializePrivateKey(privateKey, password)
  privateKey = decryptPrivateKey(encryptedPrivateKey, password, salt, iv)
  setCredentials(userId, privateKey, publicKey, password, iv)
  
  print('Successfully Logged in')
  # initSession(userId)

def registerFunc(username, password):
  # 1. query db to check if username exists
  # 2 create uuid
  # 3. create key pairs
  # 4. serialize key pairs
  # 5. create kdf salt
  # 6. create pk iv
  # 7. hash password
  # 8. encrypt private key
  # 9. save keys for session

  checkIfLoggedIn()

  userNameExists = checkUsernameExits(username)
  if userNameExists:
    print('Username already exists, please choose another')
    return False
  
  userId = generateUserId()
  privateKey, publicKey = generateKeyPair()
  privateSerialisedKey, publicSerialisedKey = serialiseKeyPair(publicKey, privateKey, password)
  salt = generateSalt()
  iv = generateIV()
  hashedPassword = hashPassword(password)
  encryptedPrivateKey = encryptPrivateKey(privateSerialisedKey, password, salt, iv)

  encodedEncryptedPrivateKey = base64.b64encode(encryptedPrivateKey).decode('utf-8')
  encodedPublicKey = base64.b64encode(publicSerialisedKey).decode('utf-8')

  successful = addUserToDB(userId, username, hashedPassword, salt, iv, encodedEncryptedPrivateKey, encodedPublicKey, datetime.datetime.now())
  if successful:
    print('Registration Successful')
    setCredentials(userId, privateSerialisedKey, publicSerialisedKey, password, iv)
  else:
    print('Failed To Register')
    

  # initSession(userId)

def logoutFunc():
  removeCredentials()
  print('Successfully logged out')

def userListFunc():
  users = listUsers()

  print('\nUsers:\n')

  formattedUsers = []
  if len(users) == 0:
    formattedUsers.append([user[0], user[1]])
  else:
    for user in users:
      formattedUsers.append([user[0], user[1]])

  print(tabulate(formattedUsers, headers=['username', 'userId']))

  print('\n')