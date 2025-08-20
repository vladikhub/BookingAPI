import pytest

@pytest.mark.parametrize("email, password, first_name, last_name, register_code, "
                         "login_code, status_code, logout_status_code", [
    ("user@example.com", "1234", "Ivan", "Pupkov", 200, 200, 200, 401),
    ("user@example.com", "1234", "Ivan", "Pupkov", 400, 200, 200, 401),
    ("user@example.com", "5678", "Ivan", "Pupkov", 400, 401, 401, 401),
    ("abcd", "555", "Ivan", "Pupkov", 422, 422, 401, 401),
])
async def test_auth_user_flow(
        email: str, password: str, first_name: str, last_name: str,
        register_code: int, login_code: int, status_code: int, logout_status_code: int,
        ac
):
    # Регистрация
    response = await ac.post(
        "/auth/register",
        json = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
    )
    assert response.status_code == register_code

    # Аутентификация
    response = await ac.post(
        "auth/login",
        json = {
            "email": email,
            "password": password,
        }
    )
    assert response.status_code == login_code
    if response.status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert "access_token" in res
        assert "access_token" in ac.cookies

    # Проверка пользователя
    response = await ac.get("auth/me")
    assert response.status_code == status_code
    if response.status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert "data" in res
        assert res["data"]["email"] == email
        assert res["data"]["first_name"] == first_name
        assert res["data"]["last_name"] == last_name

    # Выход пользователя
    response = await ac.post("/auth/logout")
    assert response.status_code == 200
    assert "access_token" not in response.json()
    assert "access_token" not in ac.cookies

    # Проверка пользователя
    response = await ac.get("auth/me")
    assert response.status_code == logout_status_code

