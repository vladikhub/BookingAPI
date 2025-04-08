from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров по id отеля")
async def get_rooms(
        hotel_id: int,
        db: DBDep
):
    rooms = await db.rooms.get_filtered(hotel_id=hotel_id)
    return rooms

@router.post("/{hotel_id}/rooms", summary="Добавление нового номера отелю с id")
async def add_room(
        db, DBDep,
        hotel_id: int,
        data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "На одного", "value": {
        "title": "Номер на одного",
        "description": "Номер с одной двухместной кроватью. Одна комната.",
        "price": 2500,
        "quantity": 5
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


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение конкретного номера конкретного отеля")
async def get_room(
        hotel_id: int,
        room_id: int,
        db: DBDep
):

    room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    return room

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
        "quantity": 5
    }},
    "2": {"summary": "На двоих", "value": {
            "title": "Номер на двоих",
            "description": "Номер с одной двухместной кроватью. Две комнаты.",
            "price": 5000,
            "quantity": 10
        }},
})):
    _room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())

    await db.rooms.update(_room_data, id=room_id)
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
    await db.commit()
    return {"status": "OK"}