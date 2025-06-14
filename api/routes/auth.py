import datetime

from backend.auth import *
from backend.sharedOp import checkUsernameExits
from client.cryptography.encryption import *
from client.cryptography.keyGeneration import *
from client.cryptography.hashing import *

""" def loginFunc(username, password):
  # 1. query db to check if username exists
  # 2. return the hashed password from 
  # 3. verify hashed password
  verifyPassword(hashedPassword, password)
  # 4. """

def registerFunc(username, password):
  # 1. query db to check if username exists
  # 2 create uuid
  # 3. create key pairs
  # 4. serialize key pairs
  # 5. create kdf salt
  # 6. create pk iv
  # 7. hash password
  # 8. encrypt private key
  userNameExists = checkUsernameExits(username)
  if userNameExists:
    print('Username already exists, please choose another')
    return False
  
  userId = generateUserId()
  privateKey, publicKey = generateKeyPair();
  privateSerialisedKey, publicSerialisedKey = serialiseKeyPair(publicKey, privateKey, password)
  salt = generateSalt()
  iv = generateIV()
  hashedPassword = hashPassword(password)
  encryptedPrivateKey = encryptPrivateKey(privateSerialisedKey, password, salt, iv)

  successful = addUserToDB(userId, username, hashedPassword, salt, iv, encryptedPrivateKey, publicSerialisedKey, datetime.datetime.now())
  if successful:
    print('Registration Successful')
  else:
    print('Failed To Register')



def logout():
  print('blah')