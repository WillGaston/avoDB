from argon2 import PasswordHasher

hasher = PasswordHasher()

def hashPassword(password):
  hashedPassword = hasher.hash(password)
  return hashedPassword

def verifyPassword(hashedPassword, password):
  try:
    hasher.verify(hashedPassword, password.encode())
    return True
  except Exception:
    return False