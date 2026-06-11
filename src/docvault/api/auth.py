"""Authentication API routes.

Owns HTTP behavior for registration and token issuance. Password hashing and
JWT construction live in docvault.auth modules.
"""

# TODO: import FastAPI routing primitives when phase 2 begins.
from fastapi import APIRouter
from docvault.schemas.requests import User

auth = APIRouter(
    prefix="/auth",
    tags="auth"
)

# TODO: implement POST /auth/register.
# Creates a user with a bcrypt password hash and returns non-secret user data.
@auth.post("/register")
async def register_user(user: User):
    #call a function that would register a user

    return {"email": user.email}

# TODO: implement POST /auth/token.
# Verifies credentials and returns a bearer JWT access token.
