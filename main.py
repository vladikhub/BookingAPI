
import uvicorn
from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2,"title": "Дубай", "name": "dubai"}
]


@app.get("/hotels")
def get_hotels(
     id: int | None = Query(None, description="Айдишник"),
     title: str | None = Query(None, description="Название отеля"),
):
 hotels_ = []
 for hotel in hotels:
     if id and hotel["id"] != id:
         continue
     if title and hotel["title"] != title:
         continue
     hotels_.append(hotel)
 return hotels_

@app.get("/")
def index():
    return {"home": "true"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"delete": "success"}


@app.post("/hotels")
def create_hotel(
    title: str = Body(embed=True)
):
    hotels.append({
        "id": len(hotels) + 1,
        "title": title
    })
    return {"Success": "True"}

@app.put("/hotels/{hotel_id}")
def update_hotel_all_fields(
    hotel_id: int,
    title: str = Body(),
    name: str = Body()
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return {"Update": "success"}
    return {"Error": "No such hotel"}

@app.patch("/hotels/{hotel_id}")
def update_hotel_field(
    hotel_id: int,
    title: str | None = Body(default=None, ),
    name: str | None = Body(default=None)
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title: hotel["title"] = title
            if name: hotel["name"] = name
            return {"Update": "success"}
    return {"Error": "No such hotel"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)