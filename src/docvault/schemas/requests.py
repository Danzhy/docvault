from pydantic import BaseModel

class Booking(BaseModel):
    place_id: int
    user_id: int
    from_date: str
    to_date: str