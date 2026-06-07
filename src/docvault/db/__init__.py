"""Database package.

Owns database connections, schema bootstrap helpers, and raw SQL repository
functions. Phase 1 uses raw psycopg3, and later phases continue to make database
access explicit rather than hiding it behind an ORM.
"""
