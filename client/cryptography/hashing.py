from argon2 import PasswordHasher

hasher = PasswordHasher()

def hashPassword(password):
  hashedPassword = hasher.hash(password)
  return hashedPassword

def verifyPassword(hashedPassword, password):
  return hasher.verify(hashedPassword, password)