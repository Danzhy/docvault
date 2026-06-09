from docvault.db.booking_repository import create_booking, list_bookins
import json

def create_booking_api(
        place_id: int,
        user_id: int,
        from_date: str,
        to_date: str
    ):
    
    create_booking(place_id, user_id, from_date, to_date)


def get_booklist_api(
        user_id: int = None, 
        place_id: int = None
):
    if user_id:
        bookings = list_bookins(user_id, None)
    else:
        bookings = list_bookins(None, place_id)

    bookings_obj = {
        'bookings': bookings
    }

    # json_obj = json.dumps(bookings_obj, indent=4, default=str)

    return bookings_obj

    

    