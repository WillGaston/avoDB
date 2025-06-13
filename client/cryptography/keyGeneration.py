import os
from cryptography.hazmat.primitives.asymmetric import rsa

def generateMasterKey():
  masterKeyBytes = os.urandom(32)
  return masterKeyBytes

def generateSalt():
  salt = os.urandom(16)
  return salt

def generateIV():
  iv = os.urandom(16)
  return iv

def generateKeyPair():
  privateKey = rsa.generate_private_key(
    public_exponent=65537,
    key_size=204,
  )

  publicKey = privateKey.public_key
  return privateKey, publicKey