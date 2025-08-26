from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException
from src.schemas.hotels import HotelAdd, HotelPATCH
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_date(
        self,
        pagination: PaginationDep,
        title: str | None,
        location: str | None,
        date_from: date,
        date_to: date
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 3
        return await self.db.hotels.get_filtered_by_date(
            date_from,
            date_to,
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(self, hotel_id: int):
        return self.db.hotels.get_one(id=hotel_id)

    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()

    async def add_hotel(self, hotel_data: HotelAdd):
        hotel = await self.db.hotels.add(hotel_data)
        await self.db.commit()
        return hotel

    async def update_hotel(self, hotel_data: HotelAdd, hotel_id: int):
        await self.db.hotels.update(hotel_data, id=hotel_id)
        await self.db.commit()

    async def update_hotel_partially(self, hotel_data: HotelPATCH, hotel_id: int):
        await self.db.hotels.update(hotel_data, exclude_unset=True, id=hotel_id)
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex