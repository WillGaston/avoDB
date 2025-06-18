import base64
import os
from cryptography.hazmat.primitives.asymmetric import rsa
import uuid

def generateMasterKey():
  masterKeyBytes = os.urandom(16)
  return masterKeyBytes

def generateSalt():
  salt = os.urandom(16)
  return base64.b64encode(salt).decode('utf-8')

def generateIV():
  iv = os.urandom(16)
  return base64.b64encode(iv).decode('utf-8')

def generateUserId():
  userId = uuid.uuid4()
  return str(userId)

def generateKeyPair():
  privateKey = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
  )

  publicKey = privateKey.public_key()
  return privateKey, publicKey