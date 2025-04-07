from pydantic import BaseModel, Field


class RoomAdd(BaseModel):
    title: str
    description: str | None
    price: int
    quantity: int

class Room(RoomAdd):
    id: int
    hotel_id: int

class RoomPATCH(BaseModel):
    title: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: int | None = Field(default=None)
    quantity: int | None = Field(default=None)


