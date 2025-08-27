from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import NoLeftRoomException, ObjectNotFoundException, NoLeftRoomHTTPException
from src.schemas.bookings import BookingRequest, BookingAdd
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получить все бронирования")
async def get_bookings(db: DBDep):
    bookings = BookingService(db).get_all()
    return {"status": "OK", "data": bookings}


@router.get("/me", summary="Получить бронирования пользователя")
async def get_bookings_by_user(user_id: UserIdDep, db: DBDep):
    bookings = await BookingService(db).get_filtered_by_user(user_id)
    return {"status": "OK", "data": bookings}


@router.post("", summary="Добавить бронирование")
async def create_booking(data: BookingRequest, db: DBDep, user_id: UserIdDep):
    try:
        booking = await BookingService(db).add_booking(user_id, data)
    except NoLeftRoomException:
        raise NoLeftRoomHTTPException
    return {"status": "OK", "data": booking}
