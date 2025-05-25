from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров по id отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-03-01"),
        date_to: date = Query(example="2025-03-10")
):
    rooms = await db.rooms.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение конкретного номера конкретного отеля")
async def get_room(
        hotel_id: int,
        room_id: int,
        db: DBDep
):

    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    return room


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера отелю с id")
async def add_room(
        db: DBDep,
        hotel_id: int,
        data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "На одного", "value": {
        "title": "Номер на одного",
        "description": "Номер с одной двухместной кроватью. Одна комната.",
        "price": 2500,
        "quantity": 5,
        "facilities_ids": []
    }},
    "2": {"summary": "На двоих", "value": {
            "title": "Номер на двоих",
            "description": "Номер с одной двухместной кроватью. Две комнаты.",
            "price": 5000,
            "quantity": 10
    }},
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    room = await db.rooms.add(_room_data)

    room_facilities = [RoomFacilityAdd(room_id=room.id, facility_id=fac_id) for fac_id in data.facilities_ids]
    await db.rooms_facilities.add_bulk(room_facilities)
    await db.commit()
    return room

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(
        hotel_id: int,
        room_id: int,
        db: DBDep
):

    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}




@router.put("/{hotel_id}/rooms/{room_id}", summary="Полностью перезаписать данные комнаты")
async def update_room_all_fields(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "На одного", "value": {
        "title": "Номер на одного",
        "description": "Номер с одной двухместной кроватью. Одна комната.",
        "price": 2500,
        "quantity": 5,
        "facilities_ids": [1, 2]
    }},
    "2": {"summary": "На двоих", "value": {
            "title": "Номер на двоих",
            "description": "Номер с одной двухместной кроватью. Две комнаты.",
            "price": 5000,
            "quantity": 10,
            "facilities_ids": [1, 2]
        }},
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    new_fac_ids = data.facilities_ids
    facilities = await db.rooms_facilities.get_filtered(room_id=room_id)
    old_facilities_ids = [item.facility_id for item in facilities]
    for_del_ids = []
    for_add_ids = []
    for i in new_fac_ids:
        if i not in old_facilities_ids:
            for_add_ids.append(i)
    for i in old_facilities_ids:
        if i not in new_fac_ids:
            for_del_ids.append(i)
    await db.rooms.update(_room_data, id=room_id)
    await db.rooms_facilities.delete(room_id, for_del_ids)
    if for_add_ids:
        rooms_facilities_for_add = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in for_add_ids]
        await db.rooms_facilities.add_bulk(rooms_facilities_for_add)
    await db.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично перезаписать данные комнаты")
async def update_room_field(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomPatchRequest = Body()):
    _room_data = RoomPatch(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    await db.rooms.update(_room_data, exclude_unset=True, id=room_id)
    if data.facilities_ids:

        new_fac_ids = data.facilities_ids
        facilities = await db.rooms_facilities.get_filtered(room_id=room_id)

        old_facilities_ids = [item.facility_id for item in facilities]
        for_del_ids = []
        for_add_ids = []
        for i in new_fac_ids:
            if i not in old_facilities_ids:
                for_add_ids.append(i)
        for i in old_facilities_ids:
            if i not in new_fac_ids:
                for_del_ids.append(i)
        await db.rooms_facilities.delete(room_id, for_del_ids)
        if for_add_ids:
            rooms_facilities_for_add = [RoomFacilityAdd(room_id=room_id, facility_id=f_id) for f_id in for_add_ids]
            await db.rooms_facilities.add_bulk(rooms_facilities_for_add)

    await db.commit()
    return {"status": "OK"}