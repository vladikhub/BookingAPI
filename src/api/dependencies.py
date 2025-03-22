
from typing import Annotated

from fastapi import Query, Depends, Request, HTTPException
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Страница", ge=1)]
    per_page: Annotated[int | None, Query(default=None, description="Количество отелей на одной странице", ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]

def get_token(request: Request):
    token = request.cookies.get("access_token")
    return token

def get_curr_user_id(token: str = Depends(get_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Вы не предоставили токен доступа")
    data = AuthService().decode_token(token)
    return data["user_id"]

UserIdDep = Annotated[int, Depends(get_curr_user_id)]