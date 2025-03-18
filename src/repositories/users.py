from src.models.users import UsersModel
from src.repositories.base import BaseRepository
from src.schemas.users import User


class UsersRepository(BaseRepository):
    model = UsersModel
    schema = User