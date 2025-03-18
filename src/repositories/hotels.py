from sqlalchemy import select, func

from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = Hotel

    async def get_all(self, title, location, limit, offset):
        query = select(HotelsModel).order_by(self.model.id)
        if location:
            query = query.filter(func.lower(HotelsModel.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsModel.title).contains(title.strip().lower()))
        query = (
            query.limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

