"""Authentication API routes.

Owns HTTP behavior for registration and token issuance. Password hashing and
JWT construction live in docvault.auth modules.
"""

# TODO: import FastAPI routing primitives when phase 2 begins.

# TODO: implement POST /auth/register.
# Creates a user with a bcrypt password hash and returns non-secret user data.

# TODO: implement POST /auth/token.
# Verifies credentials and returns a bearer JWT access token.
