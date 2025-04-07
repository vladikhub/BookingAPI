from fastapi import HTTPException
from sqlalchemy import select, insert, delete

from src.models.rooms import RoomsModel
from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def add(self, data: RoomAdd, *filter_by):
        query = select(HotelsModel).filter_by(id=filter_by[0])
        res = await self.session.execute(query)
        hotel = res.scalars().one_or_none()
        if hotel is None:
            raise HTTPException(status_code=404, detail="object is not found")
        add_room_stmt = insert(self.model).values(hotel_id=filter_by[0], **data.model_dump()).returning(self.model)
        res = await self.session.execute(add_room_stmt)
        room = res.scalars().one()
        return self.schema.model_validate(room, from_attributes=True)
