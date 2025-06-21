from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep, DBDep
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPATCH, Hotel, HotelAdd
from src.database import async_session_maker
from src.models.hotels import HotelsModel

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить отели")

async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
    date_from: date = Query(example="2025-03-01"),
    date_to: date = Query(example="2025-03-10")

):
    print("Идем в бд")
    per_page = pagination.per_page or 3
    return await db.hotels.get_filtered_by_date(
        date_from,
        date_to,
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}", summary="Получить отель по id")
async def get_hotel(
        hotel_id: int,
        db: DBDep
):

    hotel = db.hotels.get_one_or_none(id=hotel_id)
    return {"hotel": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель по id")
async def delete_hotel(
        hotel_id: int,
        db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"delete": "success"}


@router.post("", summary="Добавить отель")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value": {
        "title": "отель у моря",
        "location": "Сочи, ул. Бористая д.5"
    }},
    "2": {"summary": "Дубай", "value": {
        "title": "Дубай 5 звезд",
        "location": "Дубай, ул. Гипостиф д.4"
    }}

})):

    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"Success": "True", "data": hotel}


@router.put("/{hotel_id}", summary="Полностью перезаписать данные отеля")
async def update_hotel_all_fields(
        hotel_id: int,
        hotel_data: HotelAdd,
        db: DBDep
):

    await db.hotels.update(hotel_data, id=hotel_id)
    await db.commit()
    return {"Update": "success"}



@router.patch(
    "/{hotel_id}",
    summary="Частичное перезаписать данные отеля",
    description="Можно отправить name, а можно title")
async def update_hotel_field(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep
):

    await db.hotels.update(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"Update": "success"}


