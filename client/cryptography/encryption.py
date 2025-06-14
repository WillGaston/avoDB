import os
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

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

def deserializeKeyPair(publicSerialisedKey, privateSerialisedKey, password):
  privateKey = serialization.load_pem_private_key(
    privateSerialisedKey,
    password=password.encode(),
    backend=default_backend,
  )

  publicKey = serialization.load_pem_public_key(
    publicSerialisedKey,
    backend=default_backend,
  )

  return publicKey, privateKey

def encryptPrivateKey(privateKey, password, salt, iv):
  key = derivePasswordKey(password, salt)
  cipherInstance = createCipherInstance(iv, key)
  encryptor = cipherInstance.encryptor()
  paddingObject = padding.PKCS7(128).padder()
  paddedPK = paddingObject.update(privateKey) + paddingObject.finalize()
  encryptedPrivateKey = encryptor.update(paddedPK) + encryptor.finalize()

  return encryptedPrivateKey

def decryptPrivateKey(encryptedPrivateKey, password, salt, iv):
  key = derivePasswordKey(password, salt)
  cipherInstance = createCipherInstance(iv, key)
  decryptor = cipherInstance.decryptor()
  decryptedPrivateKey = decryptor.update(unpaddedPK) + decryptor.finalize()
  unpaddingObject = padding.PKCS7(128).padder()
  unpaddedPK = unpaddingObject.update(decryptedPrivateKey) + unpaddingObject.finalize()

  return unpaddedPK 

def encryptMasterKey(masterKey, publicKey):
  encryptedMasterKey = publicKey.encrypt(
    masterKey,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

  return encryptedMasterKey

def decryptMasterKey(privateKey, encryptedMasterKey):
  decryptedMasterKey = privateKey.decrypt(
    encryptedMasterKey,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )

  return decryptedMasterKey

def createCipherInstance(iv, masterKey):
  return Cipher(algorithms.AES(masterKey), modes.CBC(iv))

def encryptMessage(data, iv, masterKey):
  cipherInstance = createCipherInstance(iv, masterKey)
  encryptor = cipherInstance.encryptor()
  cipherText = encryptor.update(data.encode()) + encryptor.finalize()
  return cipherText
  
def decryptMessage(ciphertext, iv, masterKey):
  cipherInstance = createCipherInstance(iv, masterKey)
  decryptor = cipherInstance.decryptor()
  rawText = decryptor.update(ciphertext) + decryptor.finalize()
  return rawText