from datetime import date

from fastapi import HTTPException
from sqlalchemy import select, insert, delete, func
from sqlalchemy.orm import selectinload

from src.database import engine
from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel
from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomAdd, RoomWithRel


class RoomsRepository(BaseRepository):
    model = RoomsModel
    mapper = RoomDataMapper

    async def get_filtered_by_date(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsModel.id.in_(rooms_ids_to_get))
                 )
        result = await self.session.execute(query)
        return [RoomWithRel.model_validate(model, from_attributes=True) for model in result.scalars().all()]
        # print(query.compile(bind=engine, compile_kwargs={"literal_binds": True}))

    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRel.model_validate(model, from_attributes=True)

