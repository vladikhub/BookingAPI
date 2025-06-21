from src.database import async_session_maker_null_pool, async_session_maker
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import BDManager


async def test_add_hotel():
    hotel_data = HotelAdd(title="Крутой Отель", location="Сочи")
    async with BDManager(session_factory=async_session_maker_null_pool) as db:
        new_hotel = await db.hotels.add(hotel_data)
        await db.commit()
        print(f"{new_hotel=}")