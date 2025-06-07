from argon2 import PasswordHasher

def hashPassword(password):
  hasher = PasswordHasher()
  hashedPassword = hasher.hash(password)
  print(hashedPassword)
  return hashedPassword

def verifyPassword(passwordNoHash, passwordWithHash):
  hasher = PasswordHasher()
  return hasher.verify(passwordNoHash, passwordWithHash)