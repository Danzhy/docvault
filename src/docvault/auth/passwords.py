"""Password hashing helpers.

Uses bcrypt for password storage. Plaintext passwords must never be stored,
returned, logged, or compared directly to stored hashes.
"""

# TODO: import bcrypt.
from pwdlib import PasswordHash

# TODO: implement hash_password(password: str) -> str.
# Returns a bcrypt hash string that does not equal the plaintext password.

password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def validate_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)



# TODO: implement verify_password(password: str, password_hash: str) -> bool.
# Returns True only when bcrypt verifies the password against the stored hash.
