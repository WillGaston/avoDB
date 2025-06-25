import os
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

from client.cryptography.kdf import derivePasswordKey


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
  cipherInstance = createCipherInstance(iv, key)
  encryptor = cipherInstance.encryptor()
  paddingObject = sym_padding.PKCS7(128).padder()
  paddedPK = paddingObject.update(privateKey) + paddingObject.finalize()
  encryptedPrivateKey = encryptor.update(paddedPK) + encryptor.finalize()

  return encryptedPrivateKey

def decryptPrivateKey(encryptedPrivateKey, password, salt, iv):
  key = derivePasswordKey(password, salt)
  cipherInstance = createCipherInstance(iv, key)
  decryptor = cipherInstance.decryptor()
  decryptedPrivateKey = decryptor.update(encryptedPrivateKey) + decryptor.finalize()
  unpaddingObject = sym_padding.PKCS7(128).unpadder()
  unpaddedPK = unpaddingObject.update(decryptedPrivateKey) + unpaddingObject.finalize()

  return unpaddedPK 

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

def createCipherInstance(iv, masterKey):
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
  return unpaddedPK