from fastapi import HTTPException
from sqlalchemy import delete, select

from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    schema = RoomFacility

    async def delete(self, room_id: int, list_idx: list[int]):
        query = select(self.model).filter_by(room_id=room_id)
        res = await self.session.execute(query)
        objects = res.scalars().all()
        if not objects:
            raise HTTPException(status_code=404, detail="object is not found")
        delete_stmt = (
            delete(self.model)
            .filter_by(room_id=room_id)
            .filter(self.model.facility_id.in_(list_idx))
            )
        await self.session.execute(delete_stmt)

