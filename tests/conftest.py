import json
import logging

import pytest
from httpx import AsyncClient, ASGITransport

from src.api.dependencies import get_db
from src.config import settings
from src.database import engine_null_poll, Base, async_session_maker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import BDManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"

async def get_db_null_pool():
    async with BDManager(session_factory=async_session_maker_null_pool) as db:
        yield db

@pytest.fixture(scope="function")
async def db():
    async with BDManager(session_factory=async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_poll.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session", autouse=True)
async def load_data(setup_database):

    with open("tests/mock_hotels.json", "r", encoding='utf-8') as file:
        hotels = json.load(file)

    with open("tests/mock_rooms.json", "r", encoding='utf-8') as file:
        rooms = json.load(file)

    async with BDManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk([HotelAdd(**el) for el in hotels])
        await db_.rooms.add_bulk([RoomAdd(**el) for el in rooms])
        await db_.commit()

@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def register_user(load_data, ac):
    await ac.post(
        "/auth/register",
        json={
            "first_name": "Vlad",
            "last_name": "Smolkov",
            "email": "smavl.andrey@gmail.com",
            "password": "1234"
        }
    )
