from datetime import date, datetime

from pydantic import BaseModel


class BookingRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date

class BookingAdd(BookingRequest):
    user_id: int
    price: int

class Booking(BookingAdd):
    id: int
    created_at: datetime

