"""Booking-table database interactions for the phase-1 OA drill.

Uses raw psycopg3 queries. All functions receive a psycopg3 connection object
as their first argument. This module is intentionally a contract-only scaffold.
"""

# TODO: import psycopg.
from docvault.db.connection import db_connect
from psycopg import Connection, rows
from fastapi import HTTPException
from typing import List, Dict

# TODO: define a BookingRow dataclass or namedtuple that mirrors id, name,
# starts_at, ends_at, and created_at.

# TODO: implement create_booking(conn, name, starts_at, ends_at) -> BookingRow.
# Inserts a non-overlapping booking and returns the created row using RETURNING.
def create_booking(
        place_id: int,
        user_id: int,
        from_date: str,
        to_date: str
    ):
    conn: Connection = db_connect()

    with conn.cursor() as cur:

        cur.execute("""
            SELECT * FROM bookings
            WHERE time_to > %s::timestamp
                AND place_id = %s
        """, (from_date, place_id))

        clash = cur.fetchone()#

        if clash:
            raise HTTPException(status_code=409, detail="запрашиваемый интервал пересекается с существующим бронированием для этого места.")

        cur.execute("""
            INSERT INTO bookings (user_id, place_id, time_from, time_to)
            VALUES (%s, %s, %s, %s)
        """, (user_id, place_id, from_date, to_date))
    
        conn.commit()


# TODO: implement list_bookings(conn) -> list[BookingRow].
# Returns all bookings ordered by starts_at ascending, then id ascending.
        
def list_bookins(
        user_id: int = None,
        place_id: int = None
) -> List[Dict]:
    conn: Connection = db_connect()

    with conn.cursor(row_factory=rows.dict_row) as cur:
        
        if user_id: 
            cur.execute("""
                SELECT * FROM bookings
                WHERE user_id = %s
                ORDER BY time_from ASC, id ASC
            """, (user_id, ))

        else:
            cur.execute("""
                SELECT * FROM bookings
                WHERE place_id = %s
                ORDER BY time_from ASC, id ASC
            """, (place_id, ))

        all_bookings = cur.fetchall()

        return all_bookings



# TODO: implement has_overlap(conn, starts_at, ends_at) -> bool.
# Returns True when an existing interval overlaps the requested interval.
