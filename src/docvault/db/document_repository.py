"""Document-table database interactions.

Owns raw SQL for creating, listing, fetching, and authorizing documents. All
functions receive an open psycopg3 connection object as their first argument.
"""

# TODO: import psycopg.

# TODO: define a DocumentRow dataclass or namedtuple that mirrors the documents table.

# TODO: implement create_document(conn, owner_id, title, body) -> DocumentRow.
# Inserts a document for owner_id and returns the created row using RETURNING.

# TODO: implement list_documents_for_owner(conn, owner_id) -> list[DocumentRow].
# Returns only documents owned by owner_id ordered by created_at ascending.

# TODO: implement get_document_by_id(conn, document_id) -> DocumentRow | None.
# Returns None when no row exists; authorization is checked by the caller.

# TODO: implement get_document_for_owner(conn, document_id, owner_id) -> DocumentRow | None.
# Returns a document only when it exists and belongs to owner_id.
