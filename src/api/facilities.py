from fastapi import APIRouter, Body
import json

from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.init import redis_manager
from src.tasks.tasks import test_task


router = APIRouter(prefix="/facilities", tags=["Удобства"])



@router.get("")

async def get_facilities(db: DBDep):
    print("ИДЕМ В БД")
    return await db.facilities.get_all()



@router.post("")
async def create_facility(db: DBDep, facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facility}