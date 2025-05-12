from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "OK", "data": bookings}

@router.get("/me", summary="Получить бронирования пользователя")
async def get_bookings_by_user(
        user_id: UserIdDep,
        db: DBDep
):
    bookings = await db.bookings.get_filtered(user_id=user_id)
    return {"status": "OK", "data": bookings}

@router.post("", summary="Добавить бронирование")
async def create_booking(
        data: BookingRequest,
        db: DBDep,
        user_id: UserIdDep
):
    price = (await db.rooms.get_one_or_none(id=data.room_id)).price
    _booking_data = BookingAdd(**data.model_dump(), user_id=user_id, price=price)

    booking = await db.bookings.add(_booking_data, price)
    await db.commit()
    return booking

