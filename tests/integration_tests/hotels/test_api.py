async def test_get_hotels(ac):
    response = await ac.get("/hotels", params={"date_from": "2025-06-20", "date_to": "2025-06-25"})
    print(f"{response.json()=}")
    assert response.status_code == 200
