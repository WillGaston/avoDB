from tabulate import tabulate
import base64
import re

from backend.auth import checkDBBelongsToUser, checkRowBelongsToUser, checkTBBelongsToUser
from backend.db import *
from backend.rows import deleteRow, insertRow, listRows, selectRows
from backend.tables import *
from client.cryptography.encryption import decryptMessage, decryptPrivateKey, decryptWithPrivateKey, encryptMessage, encryptWithPublicKey
from client.cryptography.keyGeneration import generateIV, generateMasterKey, generateUserId
from client.storage.sessionManagement import *


def createDB(dbName):
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

  encryptedDBName = encryptMessage(dbName, iv, masterKey, getPrivateKey())
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
    dbname = decryptMessage(item[1], iv, masterKey, getPublicKey())
    dbDecrypted.append([item[0], dbname])

  print(tabulate(dbDecrypted, headers=["DB_id", "dbName"]))

def deleteDBR(dbId):
  userId = getUserID()
  deleteDB(userId, dbId)

def createTableRoute(dbId, tbName, schema):
  if not checkDBBelongsToUser(getUserID(), dbId):
    print('Database does not belong to you. Please choose another')
    sys.exit(1)

  encryptedMasterKey = base64.b64decode(getMasterKey(dbId))
  masterKey = decryptWithPrivateKey(getPrivateKey(), encryptedMasterKey, getPassword())

  encryptedTableName = encryptMessage(tbName, getIV(), masterKey, getPrivateKey())
  encryptedSchema = encryptMessage(schema, getIV(), masterKey, getPrivateKey())

  addTable(generateUserId(), dbId, encryptedTableName, encryptedSchema)

def deleteTableRoute(dbId, tbId):
  if not checkDBBelongsToUser(getUserID(), dbId):
    print('Database does not belong to you. Please choose another')
    sys.exit(1)

  deleteTable(dbId, tbId)

def listTablesRoute(dbId):
  if not checkDBBelongsToUser(getUserID(), dbId):
    print('Database does not belong to you. Please choose another')
    sys.exit(1)

  privateKey = getPrivateKey()
  iv = getIV()
  password = getPassword()

  encryptedMasterKey = base64.b64decode(getMasterKey(dbId))
  masterKey = decryptWithPrivateKey(privateKey, encryptedMasterKey, password)
  publicKey = getPublicKey()

  tables = listTables(dbId)

  tablesDecrypted = []

  for item in tables:
    tbname = decryptMessage(item[1], iv, masterKey, publicKey)
    schema = decryptMessage(item[2], iv, masterKey, publicKey)
    tablesDecrypted.append([item[0], tbname, schema])

  print(tabulate(tablesDecrypted, headers=["tableId", "tableName", "tableSchema"]))

def getSchemaRoute(dbId, tbId):
  if checkDBBelongsToUser(getUserID(), dbId) == 0:
    print('Database does not belong to you. Please choose another')
    sys.exit(1)
  if checkTBBelongsToUser(getUserID(), tbId) == 0:
    print('Table does not belong to you/this database or does not exist. Please choose another')
    sys.exit(1)

  encryptedMasterKey = base64.b64decode(getMasterKey(dbId))
  masterKey = decryptWithPrivateKey(getPrivateKey(), encryptedMasterKey, getPassword())
  encryptedSchema = getSchema(tbId, dbId)

  print('\nSchema:\n',decryptMessage(encryptedSchema, getIV(), masterKey, getPublicKey()).decode('utf-8'), '\n')

def rwInsertRoute(dbId, tbId, data):
  # 1. check tb belongs to user
  # 2. validate data to schema
  # 3. generate iv
  # 4. generate rowId
  # 5. encrypt data
  # 6. check follows schema
  # 7. insert
  if checkDBBelongsToUser(getUserID(), dbId) == 0:
    print('Database does not belong to you. Please choose another')
    sys.exit(1)
  if checkTBBelongsToUser(getUserID(), tbId) == 0:
    print('Table does not belong to you/this database or does not exist. Please choose another')
    sys.exit(1)

  iv = generateIV()
  rowId = generateUserId()

  encryptedMasterKey = base64.b64decode(getMasterKey(dbId))
  masterKey = decryptWithPrivateKey(getPrivateKey(), encryptedMasterKey, getPassword())
  encryptedSchema = getSchema(tbId, dbId)
  decryptedSchema = decryptMessage(encryptedSchema, getIV(), masterKey, getPublicKey()).decode('utf-8')

  if data.count(',') != decryptedSchema.count(','):
    print('Incorrect number of rows')
    sys.exit(1)

  encryptedData = encryptMessage(data, iv, masterKey, getPrivateKey())

  insertRow(rowId, tbId, encryptedData, iv)

def rwDeleteRoute(dbId, tbId, rwId):
  # 1. check row belongs to user
  # 2. delete

  if checkDBBelongsToUser(getUserID(), dbId) == 0:
    print('Database does not belong to you. Please choose another')
    sys.exit(1)
  if checkTBBelongsToUser(getUserID(), tbId) == 0:
    print('Table does not belong to you/this database or does not exist. Please choose another')
    sys.exit(1)
  if checkRowBelongsToUser(getUserID(), rwId) == 0:
    print('Table does not belong to you/this database or does not exist. Please choose another')
    sys.exit(1)

  deleteRow(tbId, rwId)

def selectRoute(dbId, tbId):
  # 1. check tb belongs to id
  # 2. get array of rows
  # 3. loop and decrypt
  # 4. get schema
  # 5. display

  if checkDBBelongsToUser(getUserID(), dbId) == 0:
    print('Database does not belong to you. Please choose another')
    sys.exit(1)
  if checkTBBelongsToUser(getUserID(), tbId) == 0:
    print('Table does not belong to you/this database or does not exist. Please choose another')
    sys.exit(1)

  privateKey = getPrivateKey()
  publicKey = getPublicKey()
  password = getPassword()

  encryptedMasterKey = base64.b64decode(getMasterKey(dbId))
  masterKey = decryptWithPrivateKey(privateKey, encryptedMasterKey, password)

  encryptedSchema = getSchema(tbId, dbId)
  decryptedSchema = decryptMessage(encryptedSchema, getIV(), masterKey, publicKey).decode('utf-8')

  schemaAttributes = decryptedSchema.split(',')
  encryptedRows = selectRows(tbId)
  decryptedRows = []


  encryptedTableName = getTableName(dbId, tbId)
  decryptedTableName = decryptMessage(encryptedTableName, getIV(), masterKey, publicKey).decode('utf-8')
  print(f'\n{decryptedTableName}:\n')

  for item in encryptedRows:
    data = decryptMessage(item[0], item[1], masterKey, publicKey).decode('utf-8').split(',')
    decryptedRows.append(data)

  print(tabulate(decryptedRows, headers=schemaAttributes))

def listRowsRoute(dbId, tbId):
  if checkDBBelongsToUser(getUserID(), dbId) == 0:
    print('Database does not belong to you. Please choose another')
    sys.exit(1)
  if checkTBBelongsToUser(getUserID(), tbId) == 0:
    print('Table does not belong to you/this database or does not exist. Please choose another')
    sys.exit(1)

  privateKey = getPrivateKey()
  publicKey = getPublicKey()
  password = getPassword()

  encryptedMasterKey = base64.b64decode(getMasterKey(dbId))
  masterKey = decryptWithPrivateKey(privateKey, encryptedMasterKey, password)

  encryptedSchema = getSchema(tbId, dbId)
  decryptedSchema = decryptMessage(encryptedSchema, getIV(), masterKey, publicKey).decode('utf-8')

  schemaAttributes = decryptedSchema.split(',')
  encryptedRows = listRows(tbId)
  decryptedRows = []

  schemaAttributes.insert(0, 'rowId')

  encryptedTableName = getTableName(dbId, tbId)
  decryptedTableName = decryptMessage(encryptedTableName, getIV(), masterKey, publicKey).decode('utf-8')
  print(f'\n{decryptedTableName}:\n')

  for item in encryptedRows:
    data = decryptMessage(item[0], item[1], masterKey, publicKey).decode('utf-8')
    decryptedRows.append([item[2], data])

  print(tabulate(decryptedRows, headers=schemaAttributes))