"""Document API routes.

Owns HTTP behavior for creating, listing, reading, and searching documents.
Authorization decisions must ensure users can only access their own documents.
"""

# TODO: import FastAPI routing primitives when phase 2 begins.

# TODO: implement POST /documents.
# Creates a document for the authenticated user and returns the created record.

# TODO: implement GET /documents.
# Lists only the authenticated user's documents.

# TODO: implement GET /documents/{document_id}.
# Returns 404 if missing and 403 if the document belongs to another user.

# TODO: in phase 4, implement POST /search.
# Searches the authenticated user's document chunks and returns ranked results.
