from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
import jwt

from src.config import settings
from src.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsException, \
    IncorrectPasswordException
from src.schemas.users import UserRegister, UserRequestRegister, UserLogin
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def decode_token(self, token: str | None) -> dict[str:str]:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")

    async def register_user(self, data: UserRequestRegister):
        hashed_password = AuthService().hash_password(data.password)
        new_user = UserRegister(
            email=data.email,
            hashed_password=hashed_password,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        try:
            await self.db.users.add(new_user)
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex
        await self.db.commit()

    async def login_user(self, data: UserLogin):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = AuthService().create_access_token({"user_id": user.id})
        await self.db.commit()
        return access_token

    async def get_one_or_none(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)

