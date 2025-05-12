from datetime import date

from sqlalchemy import select, func

from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = Hotel

    async def get_all(self, title, location, limit, offset):
        query = select(HotelsModel).order_by(self.model.id)
        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(title.strip().lower()))
        query = (
            query.limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_filtered_by_date(
            self,
            date_from: date,
            date_to: date,
            location,
            limit,
            offset

    ):

        rooms_ids = rooms_ids_for_booking(date_from, date_to)
        hotels_ids = (
            select(RoomsModel.hotel_id)
            .select_from(RoomsModel)
            .filter(RoomsModel.id.in_(rooms_ids))
        )
        if location:
            hotels_ids = hotels_ids.filter(func.lower(HotelsModel.location).contains(location.strip().lower()))

        hotels_ids = (
            hotels_ids.limit(limit)
            .offset(offset)
        )
        return await self.get_filtered(HotelsModel.id.in_(hotels_ids))
