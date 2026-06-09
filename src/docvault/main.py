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
from fastapi import FastAPI, Query, HTTPException
from docvault.api.bookings import create_booking_api, get_booklist_api
from typing import Optional


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

@app.get('/booklist')
async def get_booklist(user_id: Optional[int] = None, place_id: Optional[int] = None):
    if not user_id and not place_id:
        raise HTTPException(status_code=400, detail="Missing query paramter: either user id or place id")
    
    if user_id:
        response_obj = get_booklist_api(user_id, None)
    else: 
        response_obj = get_booklist_api(None, place_id)
    

    return response_obj


# TODO: in phase 2, define the FastAPI application and register API routers.
# The learner writes the FastAPI app construction, route registration, and
# dependency wiring here.
