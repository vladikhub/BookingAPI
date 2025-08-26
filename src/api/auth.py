from fastapi import APIRouter
from fastapi import Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserAlreadyExistsException, \
    UserEmailAlreadyExistsHTTPException, ObjectNotFoundException, UserNotExistHTTPException, \
    IncorrectPasswordException, IncorrectPasswordHTTPException
from src.schemas.users import UserRequestRegister, UserLogin, UserRegister
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", summary="Регистрация пользователя")
async def register_user(data: UserRequestRegister, db: DBDep):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"Success": "True"}


@router.post("/login", summary="Аутентификация пользователя")
async def login_user(data: UserLogin, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data)
    except ObjectNotFoundException:
        raise UserNotExistHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


# jwt.exceptions.ExpiredSignatureError: Signature has expired


@router.get("/me", summary="Получения текущего пользователя")
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await AuthService(db).get_one_or_none(user_id)
    return {"data": user}


@router.post("/logout", summary="Выход из профиля")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
