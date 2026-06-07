"""Program entrypoints for DocVault.

Phase 1 starts as a stdlib `http.server` process for the booking OA drill.
Later phases replace that low-level server with the learner's DocVault API while
keeping this module as the place where the runnable application is assembled.
"""

# TODO: import only the libraries required by the current phase.
import os
from dotenv import load_dotenv
import http.server
import socketserver
from http import HTTPStatus
import json
from fastapi import FastAPI, Query
from docvault.api.bookings import create_booking_api

load_dotenv()

PORT = int(os.getenv('DOCVAULT_PORT'))

print(type(PORT))

# TODO: implement the phase-1 command-line entrypoint.
# It reads DOCVAULT_PORT and DATABASE_URL, starts an http.server-based service,
# and serves /ping, /book, and /booklist.

app = FastAPI()

@app.get('/ping')
async def health_check():
    return {'status': 'ok'}

@app.post('/book', status_code=200)
async def make_booking(place_id: int, user_id: int, from_date: str = Query(None, alias="from"), to_date: str = Query(None, alias="to")):
    #call db function to make a write
    create_booking_api(place_id, user_id, from_date, to_date)

    return 




# TODO: in phase 2, define the FastAPI application and register API routers.
# The learner writes the FastAPI app construction, route registration, and
# dependency wiring here.
