from datetime import date


from fastapi import APIRouter, Body, Query, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров по id отеля")
@cache(expire=5)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-03-01"),
    date_to: date = Query(example="2025-03-10"),
):
    if date_to < date_from:
        raise HTTPException(status_code=400, detail="Дата выезда должна быть позже даты въезда")
    rooms = await db.rooms.get_filtered_by_date(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )
    return rooms


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение конкретного номера конкретного отеля",
)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    room = await db.rooms.get_one_or_none_with_rels(hotel_id=hotel_id, id=room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Номер не найден")
    return room


@router.post("/{hotel_id}/rooms", summary="Добавление нового номера отелю с id")
async def add_rooms(
    db: DBDep,
    hotel_id: int,
    data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "На одного",
                "value": {
                    "title": "Номер на одного",
                    "description": "Номер с одной двухместной кроватью. Одна комната.",
                    "price": 2500,
                    "quantity": 5,
                    "facilities_ids": [],
                },
            },
            "2": {
                "summary": "На двоих",
                "value": {
                    "title": "Номер на двоих",
                    "description": "Номер с одной двухместной кроватью. Две комнаты.",
                    "price": 5000,
                    "quantity": 10,
                },
            },
        }
    ),
):
    hotel = db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Отель не найден")
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
    room = await db.rooms.add(_room_data)

    room_facilities = [
        RoomFacilityAdd(room_id=room.id, facility_id=fac_id) for fac_id in data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(room_facilities)
    await db.commit()
    return room


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    room = db.rooms.get_one_or_none(id=room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Номер не найден")
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полностью перезаписать данные комнаты")
async def update_room_all_fields(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "На одного",
                "value": {
                    "title": "Номер на одного",
                    "description": "Номер с одной двухместной кроватью. Одна комната.",
                    "price": 2500,
                    "quantity": 5,
                    "facilities_ids": [1, 2],
                },
            },
            "2": {
                "summary": "На двоих",
                "value": {
                    "title": "Номер на двоих",
                    "description": "Номер с одной двухместной кроватью. Две комнаты.",
                    "price": 5000,
                    "quantity": 10,
                    "facilities_ids": [1, 2],
                },
            },
        }
    ),
):
    room = db.rooms.get_one_or_none(id=room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Номер не найден")
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())

    await db.rooms.update(_room_data, id=room_id)
    await db.rooms_facilities.set_room_facilities(room_id, data.facilities_ids)

    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично перезаписать данные комнаты")
async def update_room_field(
    db: DBDep, hotel_id: int, room_id: int, data: RoomPatchRequest = Body()
):
    room = db.rooms.get_one_or_none(id=room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Номер не найден")
    data_dict = data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **data_dict)
    await db.rooms.update(_room_data, exclude_unset=True, id=room_id)

    if "facilities_ids" in data_dict:
        await db.rooms_facilities.set_room_facilities(room_id, data.facilities_ids)
    await db.commit()
    return {"status": "OK"}
