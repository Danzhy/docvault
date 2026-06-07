"""Learner-written unit test contracts for phase 3."""

# TODO: write a test that two concurrent requests to GET /documents do not share
# a mutable database connection object.

# TODO: write a test for the background indexing boundary.
# You may mock the task scheduler or wait for task completion, but the test must
# prove document creation triggers indexing.

# TODO: write a test that a second request to the same document does not hit the DB.
# Use a mock or spy on the DB lookup function to assert it was called only once.

# TODO: write a test that cache keys include both owner_id and document_id.
# This prevents one user's cached document from leaking to another user.
