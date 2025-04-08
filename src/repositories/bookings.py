from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    model = BookingsModel
    schema = Booking
