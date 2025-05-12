from datetime import date

from fastapi import HTTPException
from sqlalchemy import select, insert, delete, func

from src.database import engine
from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel
from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_filtered_by_date(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

        return await self.get_filtered(RoomsModel.id.in_(rooms_ids_to_get))
