from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPATCH, Hotel, HotelAdd
from src.database import async_session_maker
from src.models.hotels import HotelsModel

router = APIRouter(prefix="/hotels")


@router.get("", summary="Получить отели")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),

):
    per_page = pagination.per_page or 3
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )



@router.delete("/{hotel_id}", summary="Удалить отель по id")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"delete": "success"}


@router.post("", summary="Добавить отель")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "отель у моря",
        "location": "Сочи, ул. Бористая д.5"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Дубай 5 звезд",
        "location": "Дубай, ул. Гипостиф д.4"
    }}

})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"Success": "True", "data": hotel}


@router.put("/{hotel_id}", summary="Полностью перезаписать данные отеля")
async def update_hotel_all_fields(hotel_id: int, hotel_data: HotelAdd):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, id=hotel_id)
        await session.commit()
    return {"Update": "success"}



@router.patch(
    "/{hotel_id}",
    summary="Частичное перезаписать данные отеля",
    description="Можно отправить name, а можно title")
async def update_hotel_field(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"Update": "success"}


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        return {"hotel": hotel}