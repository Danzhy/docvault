"""Database connection helpers.

Reads DATABASE_URL from the environment and creates psycopg3 connections for
request handlers, tests, and worker code.
"""

# TODO: import os and psycopg.
import os
import psycopg
from datetime import datetime
from sqlalchemy import String
from psycopg import Connection
from sqlalchemy import create_engine, text, DateTime
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.orm import Mapped, mapped_column

from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# TODO: implement get_database_url() -> str.
# Reads DATABASE_URL and raises a clear error when it is missing.
    
# TODO: implement connect().
# Opens and returns a psycopg3 connection using get_database_url().

engine = create_engine(DATABASE_URL, echo=True)

Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

# TODO: implement run_schema(conn, schema_path) -> None.
# Executes the committed schema.sql file against the given connection.

