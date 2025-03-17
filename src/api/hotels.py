from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelPATCH, Hotel
from src.database import async_session_maker
from src.models.hotels import HotelsModel

router = APIRouter(prefix="/hotels")

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"}
]


@router.get("", summary="Получить отели")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description="Расположение отеля"),

):
    per_page = pagination.per_page or 3
    async with async_session_maker() as session:
        query = select(HotelsModel)
        if location:
            query = query.filter(HotelsModel.location.ilike(f"%{location}%"))
        if title:
            query = query.filter(HotelsModel.title.ilike(f"%{title}%"))
        query = (
            query.limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels



@router.delete("/{hotel_id}", summary="Удалить отель по id")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"delete": "success"}


@router.post("", summary="Добавить отель")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
        add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"Success": "True"}


@router.put("/{hotel_id}", summary="Полностью перезаписать данные отеля")
def update_hotel_all_fields(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            return {"Update": "success"}
    return {"Error": "No such hotel"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное перезаписать данные отеля",
    description="Можно отправить name, а можно title")
def update_hotel_field(hotel_id: int, hotel_data: HotelPATCH):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title:
                hotel["title"] = hotel_data.title
            if hotel_data.name:
                hotel["name"] = hotel_data.name
            return {"Update": "success"}
    return {"Error": "No such hotel"}