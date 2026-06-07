"""Memory storage and recall contracts.

Stores useful facts and retrieves relevant memories for later user interactions.
"""

# TODO: define a MemoryRow dataclass or namedtuple.
# Mirrors id, owner_id, source_document_id, text, and created_at.

# TODO: implement remember(conn, owner_id, text, source_document_id=None) -> MemoryRow.
# Stores a durable memory and returns the created row.

# TODO: implement recall(conn, owner_id, query, limit=3) -> list[MemoryRow].
# Returns ranked memories relevant to the query for this owner only.
