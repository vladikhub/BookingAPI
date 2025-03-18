from pydantic import BaseModel, Field

class HotelAdd(BaseModel):
    title: str
    location: str

class Hotel(BaseModel):
    id: int
    title: str
    location: str

class HotelPATCH(BaseModel):
    title: str | None = Field(default=None)
    location: str | None = Field(default=None)

