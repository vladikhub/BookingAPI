import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2025-06-07", "2025-06-15", 200),
        (1, "2025-06-08", "2025-06-16", 200),
        (1, "2025-06-09", "2025-06-17", 200),
        (1, "2025-06-10", "2025-06-18", 200),
        (1, "2025-06-11", "2025-06-19", 200),
        (1, "2025-06-12", "2025-06-20", 409),
        (1, "2025-06-16", "2025-06-26", 200),
    ],
)
async def test_add_booking(room_id, date_from, date_to, status_code, db, authed_ac):
    response = await authed_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        print(res)
        assert "data" in res


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for db_ in get_db_null_pool():
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, booked_count",
    [
        (1, "2025-06-07", "2025-06-15", 1),
        (1, "2025-06-08", "2025-06-16", 2),
        (1, "2025-06-09", "2025-06-17", 3),
    ],
)
async def test_add_and_get_my_bookings(
    room_id, date_from, date_to, booked_count, delete_all_bookings, authed_ac
):
    await authed_ac.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )
    response = await authed_ac.get("/bookings/me")
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    assert "data" in res
    data = res["data"]
    assert len(data) == booked_count
