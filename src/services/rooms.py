from datetime import date

from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException, \
    RoomNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatch, RoomPatchRequest, Room
from src.services.base import BaseService
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_date(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        check_date_to_after_date_from(date_from, date_to)
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        rooms = await self.db.rooms.get_filtered_by_date(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        return rooms

    async def get_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        return await self.db.rooms.get_one_with_rels(id=room_id)

    async def add_room(self, hotel_id: int, data: RoomAddRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        room = await self.db.rooms.add(_room_data)

        room_facilities = [
            RoomFacilityAdd(room_id=room.id, facility_id=fac_id) for fac_id in data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(room_facilities)
        await self.db.commit()
        return room

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        await self.db.commit()

    async def update_room(self, hotel_id: int, room_id: int, data: RoomAddRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())

        await self.db.rooms.update(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(room_id, data.facilities_ids)

        await self.db.commit()

    async def update_room_partially(self, hotel_id: int, room_id: int, data: RoomPatchRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        data_dict = data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **data_dict)
        await self.db.rooms.update(_room_data, exclude_unset=True, id=room_id)

        if "facilities_ids" in data_dict:
            await self.db.rooms_facilities.set_room_facilities(room_id, data.facilities_ids)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            room = await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        return room