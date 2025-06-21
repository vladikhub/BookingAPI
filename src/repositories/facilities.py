from fastapi import HTTPException
from sqlalchemy import delete, select, insert

from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    mapper = RoomFacilityDataMapper

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        cur_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(cur_facilities_ids_query)
        cur_facilities_ids = res.scalars().all()
        ids_for_del = list(set(cur_facilities_ids) - set(facilities_ids))
        ids_for_add = list(set(facilities_ids) - set(cur_facilities_ids))

        if ids_for_add:
            add_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_for_add])
            )
            await self.session.execute(add_stmt)

        if ids_for_del:
            del_stmt = (
                delete(self.model)
                .filter_by(room_id=room_id)
                .filter(self.model.facility_id.in_(ids_for_del))
            )
            await self.session.execute(del_stmt)

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

