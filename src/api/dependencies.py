from typing import Annotated

from fastapi import Query, Depends
from pydantic import BaseModel

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, description="Страница", ge=1)]
    per_page: Annotated[int | None, Query(default=None, description="Количество отелей на одной странице", ge=1, lt=30)]

PaginationDep = Annotated[PaginationParams, Depends()]