"""Authentication dependencies for protected routes.

Resolves the current user from the Authorization header and database. Route code
uses this layer to avoid duplicating token parsing and user lookup.
"""

# TODO: import the FastAPI dependency primitives when phase 2 begins.

# TODO: implement get_current_user(...).
# Reads a bearer token, decodes it, loads the matching user, and rejects invalid requests.
