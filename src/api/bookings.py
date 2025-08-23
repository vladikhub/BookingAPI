from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import NoLeftRoomException, ObjectNotFoundException
from src.schemas.bookings import BookingRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me", summary="Получить бронирования пользователя")
async def get_bookings_by_user(user_id: UserIdDep, db: DBDep):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "OK", "data": bookings}


@router.post("", summary="Добавить бронирование")
async def create_booking(data: BookingRequest, db: DBDep, user_id: UserIdDep):
    try:
        room = await db.rooms.get_one(id=data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")
    hotel_id = room.hotel_id
    price = room.price
    _booking_data = BookingAdd(**data.model_dump(), user_id=user_id, price=price)
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel_id)
    except NoLeftRoomException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}

