from datetime import date

from src.schemas.bookings import BookingAdd
from src.schemas.hotels import HotelAdd


async def test_booking_crud(db):
    # Тест create
    booking_data = BookingAdd(
        user_id= (await db.users.get_all())[0].id,
        room_id= (await db.rooms.get_all())[0].id,
        date_from= date(year=2025, month=6, day=30),
        date_to= date(year=2025, month=6, day=21),
        price= 200
    )
    new_booking = await db.bookings.add(booking_data)

    booking_id = new_booking.id
    # Тест read
    booking = await db.bookings.get_one_or_none(
        id=new_booking.id
    )
    assert booking
    assert new_booking.room_id == booking.room_id
    assert new_booking.price == booking.price

    # Тест update
    booking_update = BookingAdd(
        user_id=(await db.users.get_all())[0].id,
        room_id=(await db.rooms.get_all())[0].id,
        date_from=date(year=2025, month=6, day=25),
        date_to=date(year=2025, month=6, day=21),
        price=500
    )
    old_price = new_booking.price
    old_date = new_booking.date_from
    await db.bookings.update(booking_update, id=booking_id)
    updated_booking = await db.bookings.get_one_or_none(id=booking_id)
    assert updated_booking.price != old_price
    assert updated_booking.price == 500
    assert updated_booking.date_from != old_date
    assert updated_booking.date_from == date(year=2025, month=6, day=25)

    # Тест delete

    await db.bookings.delete(id=booking_id)

    deleted_booking = await db.bookings.get_one_or_none(id=booking_id)
    assert deleted_booking is None

