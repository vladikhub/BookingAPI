from Tools.scripts.parse_html5_entities import write_items
from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPATCH

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров по id отеля")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(hotel_id=hotel_id)
    return rooms

@router.post("/{hotel_id}/rooms", summary="Добавление нового номера отелю с id")
async def add_room(hotel_id: int, data: RoomAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(data, hotel_id)
        await session.commit()
    return room

@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "OK"}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение конкретного номера конкретного отеля")
async def get_room_by_id(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
    return room

@router.put("/{hotel_id}/rooms/{room_id}", summary="Полностью перезаписать данные комнаты")
async def update_room_all_fields(
        hotel_id: int,
        room_id: int,
        data: RoomAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        await RoomsRepository(session).update(data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частисно перезаписать данные комнаты")
async def update_room_field(
        hotel_id: int,
        room_id: int,
        data: RoomPATCH = Body()):
    async with async_session_maker() as session:
        await RoomsRepository(session).update(data, exclude_unset=True, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}