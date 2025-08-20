from datetime import date

from sqlalchemy import select, func

from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.base import DataMapper
from src.repositories.mappers.mappers import HotelDataMapper
from src.repositories.utils import rooms_ids_for_booking

class HotelsRepository(BaseRepository):
    model = HotelsModel
    mapper: DataMapper = HotelDataMapper


    async def get_filtered_by_date(
            self,
            date_from: date,
            date_to: date,
            title,
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
        query = select(HotelsModel).order_by(self.model.id).filter(HotelsModel.id.in_(hotels_ids))
        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(title.strip().lower()))
        query = (
            query.limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

