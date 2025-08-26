from datetime import date

from fastapi import Query, APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException, HotelNotExistsHTTPException
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.services.hotels import HotelService

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Получить отели")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),
    date_from: date = Query(example="2025-03-01"),
    date_to: date = Query(example="2025-03-10"),
):

    return await HotelService(db).get_filtered_by_date(
        pagination,
        title,
        location,
        date_from,
        date_to
    )


@router.get("/{hotel_id}", summary="Получить отель по id")
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        hotel = HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException:
        raise HotelNotExistsHTTPException
    return {"hotel": hotel}


@router.delete("/{hotel_id}", summary="Удалить отель по id")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id=hotel_id)
    return {"delete": "success"}


@router.post("", summary="Добавить отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "отель у моря",
                    "location": "Сочи, ул. Бористая д.5",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Дубай 5 звезд",
                    "location": "Дубай, ул. Гипостиф д.4",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data=hotel_data)
    return {"Success": "True", "data": hotel}


@router.put("/{hotel_id}", summary="Полностью перезаписать данные отеля")
async def update_hotel_all_fields(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).update_hotel(hotel_data=hotel_data, hotel_id=hotel_id)
    return {"Update": "success"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное перезаписать данные отеля",
    description="Можно отправить name, а можно title",
)
async def update_hotel_field(hotel_id: int, hotel_data: HotelPATCH, db: DBDep):
    await HotelService(db).update_hotel_partially(hotel_data=hotel_data, hotel_id=hotel_id)
    return {"Update": "success"}
