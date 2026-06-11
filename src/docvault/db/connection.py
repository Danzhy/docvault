"""Database connection helpers.

Reads DATABASE_URL from the environment and creates psycopg3 connections for
request handlers, tests, and worker code.
"""

# TODO: import os and psycopg.
import os
import psycopg
from psycopg import Connection
from dotenv import load_dotenv

load_dotenv()

# TODO: implement get_database_url() -> str.
# Reads DATABASE_URL and raises a clear error when it is missing.
DATABASE_URL = os.getenv("DATABASE_URL")

# TODO: implement connect().
# Opens and returns a psycopg3 connection using get_database_url().

def db_connect() -> Connection:
    return psycopg.connect(
    host="localhost",
    dbname="docvault",
    user="docvault",
    password="docvault"
)

# TODO: implement run_schema(conn, schema_path) -> None.
# Executes the committed schema.sql file against the given connection.
