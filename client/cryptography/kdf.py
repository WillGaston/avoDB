from argon2.low_level import hash_secret_raw, verify_secret, Type

def derivePasswordKey(password, salt):
  hashedPassword =hash_secret_raw(
    password.encode(),
    salt,
    time_cost=2,
    memory_cost=64 * 1024,
    parallelism=4,
    hash_len=32,
    type=Type.D
  )
  return hashedPassword