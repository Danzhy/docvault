"""Redis cache contracts.

Owns cache reads, writes, and invalidation for document endpoints.
"""

# TODO: import redis client helpers when phase 3 begins.

# TODO: implement get_cached_document(document_id: int, owner_id: int) -> dict | None.
# Returns cached document data for this owner/document pair or None on miss.

# TODO: implement set_cached_document(document: dict) -> None.
# Stores document data with DOCVAULT_CACHE_TTL_SECONDS.

# TODO: implement invalidate_document(document_id: int, owner_id: int) -> None.
# Removes cached data after writes.
