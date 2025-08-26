from src.exceptions import NoLeftRoomException
from src.schemas.bookings import BookingRequest, BookingAdd
from src.services.base import BaseService
from src.services.rooms import RoomService


class BookingService(BaseService):
    async def get_all(self):
        return await self.db.bookings.get_all()

    async def get_filtered_by_user(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, user_id: int, data: BookingRequest):
        room = await RoomService(self.db).get_room_with_check(room_id=data.room_id)
        hotel_id = room.hotel_id
        price = room.price
        _booking_data = BookingAdd(**data.model_dump(), user_id=user_id, price=price)
        booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel_id)
        await self.db.commit()
        return booking