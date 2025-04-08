from fastapi import HTTPException
from sqlalchemy import select, insert, delete

from src.models.rooms import RoomsModel
from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room


