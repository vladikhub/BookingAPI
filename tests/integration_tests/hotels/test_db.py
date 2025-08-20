from src.schemas.hotels import HotelAdd


async def test_add_hotel(db):
    hotel_data = HotelAdd(title="Крутой Отель", location="Сочи")
    new_hotel = await db.hotels.add(hotel_data)
    await db.commit()
    print(f"{new_hotel=}")
