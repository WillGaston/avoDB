from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

def createKDFInstance(salt):
  argonKDF = Argon2id(
    salt = salt,
    length = 32,
    iterations = 1,
    lanes = 4,
    memory_cost = 64 * 1024,
    ad = None,
    secret = None,
  )

  return argonKDF

def hashPassword(password, salt):
  kdf = createKDFInstance(salt)
  hashedPassword = kdf.derive(password.decode())
  return hashedPassword

def verifyPassword(passwordToTest, hashedPassword, salt):
  kdf = createKDFInstance(salt)
  return kdf.verify(passwordToTest.decode(), hashedPassword)