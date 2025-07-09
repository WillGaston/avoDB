import sys
import base64
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag, InvalidSignature
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

from client.cryptography.kdf import derivePasswordKey
from client.storage.sessionManagement import getPassword


def serialiseKeyPair(publicKey, privateKey, password):
  privateSerialisedKey = privateKey.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.PKCS8,
    encryption_algorithm = serialization.BestAvailableEncryption(password.encode())
  )

  publicSerialisedKey = publicKey.public_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PublicFormat.SubjectPublicKeyInfo,
  )

  return privateSerialisedKey, publicSerialisedKey

def serialisePrivateKey(privateKey, password):
  privateSerialisedKey = privateKey.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.PKCS8,
    encryption_algorithm = serialization.BestAvailableEncryption(password.encode())
  )

  return privateSerialisedKey

def deserializeKeyPair(publicSerialisedKey, privateSerialisedKey, password):
  privateKey = serialization.load_pem_private_key(
    privateSerialisedKey,
    password=password.encode(),
    backend=default_backend(),
  )

  publicKey = serialization.load_pem_public_key(
    publicSerialisedKey,
    backend=default_backend(),
  )

  return publicKey, privateKey

def deserialisePrivateKey(privateSerialisedKey, password):
  privateKey = serialization.load_pem_private_key(
    privateSerialisedKey,
    password=password,
    backend=default_backend(),
  )

  return privateKey

def deserialisePublicKey(publicSerialisedKey):
  publicKey = serialization.load_pem_public_key(
    publicSerialisedKey,
    backend=default_backend(),
  )
  return publicKey

def encryptPrivateKey(privateKey, password, salt, iv):
  key = derivePasswordKey(password, salt)
  iv = base64.b64decode(iv)
  gcmKey = AESGCM(key)
  encryptedPrivateKey = gcmKey.encrypt(iv, privateKey, associated_data=None)

  return encryptedPrivateKey

def decryptPrivateKey(encryptedPrivateKey, password, salt, iv):
  key = derivePasswordKey(password, salt)
  iv = base64.b64decode(iv)
  gcmKey = AESGCM(key)
  try:
    decryptedPrivateKey = gcmKey.decrypt(iv, encryptedPrivateKey, associated_data=None)
  except InvalidTag:
    print('Tampering of ciphertext detected')
    sys.exit(1)

  return decryptedPrivateKey 

def encryptWithPublicKey(item, publicKey):
  deserialisedPublicKey = deserialisePublicKey(publicKey)
  encryptedItem = deserialisedPublicKey.encrypt(
    item,
    asym_padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

  return encryptedItem

def decryptWithPrivateKey(privateKey, encryptedItem, password):
  deserialisedPrivateKey = deserialisePrivateKey(privateKey, password)
  decryptedItem = deserialisedPrivateKey.decrypt(
    encryptedItem,
    asym_padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

  return decryptedItem

# Previous Encryption mechanism using CBC + padding
# - does not provide integrity / authentication / non-repudiation
""" def createCipherInstance(iv, masterKey):
  return Cipher(algorithms.AES(masterKey), modes.CBC(base64.b64decode(iv)))

def encryptMessage(data, iv, masterKey):
  cipherInstance = createCipherInstance(iv, masterKey)
  encryptor = cipherInstance.encryptor()
  paddingObject = sym_padding.PKCS7(128).padder()
  paddedData = paddingObject.update(data.encode()) + paddingObject.finalize()
  cipherText = encryptor.update(paddedData) + encryptor.finalize()
  return base64.b64encode(cipherText).decode('utf-8')
  
def decryptMessage(ciphertext, iv, masterKey):
  cipherInstance = createCipherInstance(iv, masterKey)
  decryptor = cipherInstance.decryptor()
  rawText = decryptor.update(base64.b64decode(ciphertext)) + decryptor.finalize()
  unpaddingObject = sym_padding.PKCS7(128).unpadder()
  unpaddedPK = unpaddingObject.update(rawText) + unpaddingObject.finalize()
  return unpaddedPK """

def encryptMessage(data, iv, masterKey, privateKey):
  gcmKey = AESGCM(masterKey)
  iv = base64.b64decode(iv)
  deserialisedPrivateKey = deserialisePrivateKey(privateKey, getPassword())
  encoded_data = data.encode('utf-8')
  signature = getSignature(deserialisedPrivateKey, encoded_data)

  signedData = json.dumps({
    "data": base64.b64encode(encoded_data).decode('utf-8'),
    "signature": base64.b64encode(signature).decode('utf-8')
  }).encode('utf-8')

  cipherText = gcmKey.encrypt(iv, signedData, associated_data=None)

  return base64.b64encode(cipherText).decode('utf-8')
  
def decryptMessage(ciphertext, iv, masterKey, publicKey):
  gcmKey = AESGCM(masterKey)
  iv = base64.b64decode(iv)
  try:
    decodedText = gcmKey.decrypt(iv, base64.b64decode(ciphertext), associated_data=None)
  except InvalidTag:
    print('Tampering of ciphertext detected')
    sys.exit(1)

  deBundledData = json.loads(decodedText.decode('utf-8'))
  data = base64.b64decode(deBundledData["data"])
  signature = base64.b64decode(deBundledData["signature"])

  deserialisedPublicKey = deserialisePublicKey(publicKey)

  try:
    verifySignature(deserialisedPublicKey, signature, data)
  except InvalidSignature:
    print('Invalid signature in data')
    sys.exit(1)

  return data

def getSignature(privateKey, data):
  signature = privateKey.sign(
    data,
    padding.PSS(
      mgf=padding.MGF1(hashes.SHA256()),
      salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
  )

  return signature

def verifySignature(publicKey, signature, data):
  try:
    publicKey.verify(
      signature,
      data,
      padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
      ),
      hashes.SHA256()
    )
  except InvalidSignature:
    raise
