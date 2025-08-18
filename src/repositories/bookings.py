from datetime import date

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert
from sqlalchemy.exc import IntegrityError

from src.exceptions import NoLeftRoomException
from src.models import HotelsModel, RoomsModel
from src.models.bookings import BookingsModel
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import Booking
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsModel)
            .filter(BookingsModel.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in res.scalars().all()]


    async def add_booking(self, **data):

        try:
            rooms_ids = rooms_ids_for_booking(date_from=data["date_from"], date_to=data["date_to"])
            query = select(RoomsModel.id).filter(RoomsModel.id.in_(rooms_ids))
            res = await self.session.execute(query)
            rooms_ids = res.scalars().all()
            if data["room_id"] in rooms_ids:
                add_data_stmt = insert(self.model).values(**data).returning(self.model)
                #print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
                res = await self.session.execute(add_data_stmt)
                model = res.scalars().one()
                return self.mapper.map_to_domain_entity(model)
            else:
                raise NoLeftRoomException()
        except IntegrityError:
            raise HTTPException(status_code=404, detail="object is not found")



