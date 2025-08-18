


async def test_add_booking(db, authed_ac):
    room_id = (await db.rooms.get_all())[0].id

    response = await authed_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2025-06-22",
            "date_to": "2025-06-25"
        }
    )

    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)
    print(res)
    assert "data" in res
