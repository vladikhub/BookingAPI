from os import access

from fastapi import Query, APIRouter, Body, HTTPException, Depends
from fastapi import Response, Request

from src.api.dependencies import UserIdDep, DBDep
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestRegister, UserLogin, UserRegister
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register", summary="Регистрация пользователя")
async def register_user(
        data: UserRequestRegister,
        db: DBDep
):
    hashed_password = AuthService().hash_password(data.password)
    new_user = UserRegister(
        email=data.email,
        hashed_password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name
    )

    await db.users.add(new_user)
    await db.commit()
    return {"Success": "True"}

@router.post("/login", summary="Аутентификация пользователя")
async def login_user(
        data: UserLogin,
        response: Response,
        db: DBDep
):

    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    await db.commit()
    return {"access_token": access_token}

# jwt.exceptions.ExpiredSignatureError: Signature has expired


@router.get("/me", summary="Получения текущего пользователя")
async def get_me(
        user_id: UserIdDep,
        db: DBDep
):

    user = await db.users.get_one_or_none(id=user_id)
    return {"data": user}



@router.post("/logout", summary="Выход из профиля")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}