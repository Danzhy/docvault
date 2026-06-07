"""User-table database interactions.

Owns raw SQL for user registration and lookup. Authentication code calls this
module, but password hashing and token logic live in the auth package.
"""

# TODO: import psycopg.

# TODO: define a UserRow dataclass or namedtuple that mirrors the users table.

# TODO: implement create_user(conn, email, password_hash) -> UserRow.
# Inserts a user and returns the created row using RETURNING.

# TODO: implement get_user_by_email(conn, email) -> UserRow | None.
# Returns None when no user matches.

# TODO: implement get_user_by_id(conn, user_id) -> UserRow | None.
# Returns None when no user matches.
