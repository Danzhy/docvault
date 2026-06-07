"""Document indexing worker contracts.

Turns documents into searchable chunks after writes. Phase 3 schedules this work
in the background; phase 4 fills in chunking and embedding behavior.
"""

# TODO: implement enqueue_document_index(document_id: int) -> None.
# Schedules indexing work without blocking the HTTP response.

# TODO: implement index_document(document_id: int) -> None.
# Loads a document, chunks it, embeds chunks, and stores them for retrieval.
