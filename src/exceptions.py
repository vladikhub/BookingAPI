class MyBookingsException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(MyBookingsException):
    detail = "Объект не найден"


class NoLeftRoomException(MyBookingsException):
    detail = "Нет свободных номеров"

