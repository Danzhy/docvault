from docvault.db.booking_repository import create_booking

def create_booking_api(
        place_id: int,
        user_id: int,
        from_date: str,
        to_date: str
    ):
    
    create_booking(place_id, user_id, from_date, to_date)
    

    