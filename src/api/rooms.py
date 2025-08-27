from datetime import date


from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    RoomNotExistsHTTPException,
    HotelNotExistsHTTPException,
    HotelNotFoundException,
    RoomNotFoundException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", summary="Получение всех номеров по id отеля")
@cache(expire=5)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2025-03-01"),
    date_to: date = Query(example="2025-03-10"),
):
    try:
        rooms = await RoomService(db).get_filtered_by_date(hotel_id, date_from, date_to)
    except HotelNotFoundException:
        raise HotelNotExistsHTTPException
    return rooms


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение конкретного номера конкретного отеля",
)
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        room = await RoomService(db).get_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotExistsHTTPException
    except RoomNotFoundException:
        raise RoomNotExistsHTTPException
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
    try:
        room = await RoomService(db).add_room(hotel_id, data)
    except HotelNotFoundException:
        raise HotelNotExistsHTTPException
    return room


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление номера")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    try:
        await RoomService(db).delete_room(hotel_id, room_id)
    except HotelNotFoundException:
        raise HotelNotExistsHTTPException
    except RoomNotFoundException:
        raise RoomNotExistsHTTPException
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
    try:
        await RoomService(db).update_room(hotel_id, room_id, data)
    except HotelNotFoundException:
        raise HotelNotExistsHTTPException
    except RoomNotFoundException:
        raise RoomNotExistsHTTPException
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частично перезаписать данные комнаты")
async def update_room_field(
    db: DBDep, hotel_id: int, room_id: int, data: RoomPatchRequest = Body()
):
    try:
        await RoomService(db).update_room_partially(hotel_id, room_id, data)
    except HotelNotFoundException:
        raise HotelNotExistsHTTPException
    except RoomNotFoundException:
        raise RoomNotExistsHTTPException
    return {"status": "OK"}
