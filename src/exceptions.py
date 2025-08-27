from datetime import date

from fastapi import HTTPException


class MyBookingsException(Exception):
    status_code = 500
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MyBookingsException):
    detail = "Объект не найден"


class RoomNotFoundException(MyBookingsException):
    detail = "Номер не найден"


class HotelNotFoundException(MyBookingsException):
    detail = "Отель не найден"


class NoLeftRoomException(MyBookingsException):
    detail = "Нет свободных номеров"


class ObjectAlreadyExistsException(MyBookingsException):
    detail = "Такой объект уже существует"


class UserAlreadyExistsException(MyBookingsException):
    detail = "Такой пользователь уже существует"


class IncorrectPasswordException(MyBookingsException):
    detail = "Пароль неверный"


def check_date_to_after_date_from(date_from: date, date_to: date):
    if date_to <= date_from:
        raise HTTPException(status_code=400, detail="Дата выезда должна быть позже даты въезда")


class MyBookingsHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self, *args, **kwargs):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotExistsHTTPException(MyBookingsHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotExistsHTTPException(MyBookingsHTTPException):
    status_code = 404
    detail = "Номер не найден"


class NoLeftRoomHTTPException(MyBookingsHTTPException):
    status_code = 409
    detail = "Нет свободных номеров"


class UserEmailAlreadyExistsHTTPException(MyBookingsHTTPException):
    status_code = 409
    detail = "Пользователь с таким email уже существует"


class UserNotExistHTTPException(MyBookingsHTTPException):
    status_code = 404
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordHTTPException(MyBookingsHTTPException):
    status_code = 401
    detail = "Пароль неверный"
