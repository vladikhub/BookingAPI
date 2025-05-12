from datetime import date

from fastapi import HTTPException
from sqlalchemy import select, insert, delete, func

from src.database import engine
from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel
from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room, RoomAdd

def rooms_ids_for_booking(
        date_from: date,
        date_to: date,
        hotel_id: int | None = None,
):
    booked_rooms = (
        select(BookingsModel.room_id, func.count("*").label("count_booked"))
        .select_from(BookingsModel)
        .filter(
            BookingsModel.date_from <= date_to,
            BookingsModel.date_to >= date_from
        )
        .group_by(BookingsModel.room_id)
        .cte(name="booked_rooms")
    )
    left_rooms = (
        select(RoomsModel.id.label("room_id"),
        (RoomsModel.quantity - func.coalesce(booked_rooms.c.count_booked, 0)).label("rooms_left"))
        .select_from(RoomsModel)
        .outerjoin(booked_rooms, RoomsModel.id == booked_rooms.c.room_id)
        .cte(name="left_rooms")
    )

    rooms_ids_for_hotel = (
        select(RoomsModel.id)
    )

    if hotel_id:
        rooms_ids_for_hotel = (
            rooms_ids_for_hotel
            .filter_by(hotel_id=hotel_id)
        )

    rooms_ids_for_hotel = (
        rooms_ids_for_hotel
        .subquery(name="rooms_ids_for_hotel")
    )

    rooms_ids_to_get = (
        select(left_rooms.c.room_id)
        .select_from(left_rooms)
        .filter(
            left_rooms.c.rooms_left > 0,
            left_rooms.c.room_id.in_(rooms_ids_for_hotel)
        )
    )
    return rooms_ids_to_get