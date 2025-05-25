from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (select(self.model)
                .filter(*filter)
                .filter_by(**filter_by)
                .order_by(self.model.id))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def add(self, data: BaseModel, *args):
        try:
            add_data_stmt = insert(self.model).values( **data.model_dump()).returning(self.model)
            #print(add_hotel_stmt.compile(compile_kwargs={"literal_binds": True}))
            res = await self.session.execute(add_data_stmt)
        except IntegrityError:
            raise HTTPException(status_code=404, detail="object is not found")
        model = res.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def add_bulk(self, data: list[BaseModel], *args):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def update(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        objects = res.scalars().all()
        if not objects:
            raise HTTPException(status_code=404, detail="object is not found")
        if len(objects) > 1:
            raise HTTPException(status_code=400, detail="must be one object")
        update_data_stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        # print(update_data_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_data_stmt)

    async def delete(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        objects = res.scalars().all()
        if not objects:
            raise HTTPException(status_code=404, detail="object is not found")
        if len(objects) > 1:
            raise HTTPException(status_code=400, detail="must be one object")
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        # print(update_data_stmt.compile(compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_data_stmt)
