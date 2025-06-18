from tabulate import tabulate
import base64

from backend.db import addDB, deleteDB, listDBs
from client.cryptography.encryption import decryptMessage, decryptWithPrivateKey, encryptMessage, encryptWithPublicKey
from client.cryptography.keyGeneration import generateIV, generateMasterKey, generateUserId
from client.storage.sessionManagement import *


def createDB(dbName):
  print('blah')
  # 1. generate master key
  # 2. generate iv
  # 3. generate db id
  # 4. encrypt db name
  # 5. encrypt master key
  # 6. create db via backend

  # check if user already has db with this name

  masterKey = generateMasterKey()
  iv = generateIV()
  dbId = generateUserId()

  publicKey = getPublicKey()
  userId = getUserID()
  iv = getIV()

  encryptedDBName = encryptMessage(dbName, iv, masterKey)
  encryptedMasterKey = encryptWithPublicKey(masterKey, publicKey)

  result = addDB(dbId, userId, iv, encryptedDBName, base64.b64encode(encryptedMasterKey).decode('utf-8'))

  if not result:
    # error
    print('did not add db')


def listDB():
  userId = getUserID()
  privateKey = getPrivateKey()
  iv = getIV()
  password = getPassword()

  DBs = listDBs(userId)

  dbDecrypted = []

  for item in DBs:
    masterKey = decryptWithPrivateKey(privateKey, base64.b64decode(item[2]), password)
    dbname = decryptMessage(item[1], iv, masterKey)
    dbDecrypted.append([item[0], base64.b64encode(dbname)])

  print(tabulate(dbDecrypted, headers=["DB_id", "dbName"]))

def deleteDBR(dbId):
  userId = getUserID()
  deleteDB(userId, dbId)
