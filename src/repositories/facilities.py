from src.models.facilities import FacilitiesModel
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    schema = Facility