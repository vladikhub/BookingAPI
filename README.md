# 🏨 Hotel Booking API 

**Сервис бронирования отелей**, реализованный на FastAPI с асинхронной архитектурой, JWT-авторизацией и работой с PostgreSQL. (в процессе разработки)

---

## 🚀 Технологии

- ⚙️ **Python**, **FastAPI**
- 🗄 **PostgreSQL** + **SQLAlchemy (async)**
- 🧪 **Alembic** (миграции)
- 🔐 **JWT** авторизация + куки
- ⚒ **Слоистая архитектура**: repository → service → API
- 💉 **Dependency Injection** через FastAPI Depends
- 🔍 Фильтрация, пагинация

---

## 📚 Функциональность

- 🔐 Регистрация и авторизация (JWT токены выдаются в cookies)
- 🏨 Работа с отелями и номерами
  - CRUD отелей
  - CRUD номеров
  - Фильтрация по параметрам 
- 📅 Бронирование номеров
- 👤 Просмотр своих бронирований (доступен только авторизованному пользователю)
- 🧱 Четкая архитектура проекта 

---
## Документация ручек
### Авторизация и аутентификация:
  - POST /auth/register
  - POST /auth/login
  - GET /auth/me
  - POST /auth/logout
### Отели:
  - GET /hotels
  - POST /hotels
  - GET /hotels/(hotel_id)
  - DELETE /hotels/(hotel_id)
  - PUT /hotels/(hotel_id)
  - PATCH /hotels/(hotel_id)
### Номера:
  - GET /hotels/{hotel_id}/rooms
  - POST /hotels/{hotel_id}/rooms
  - GET /hotels/{hotel_id}/rooms/{room_id}
  - DELETE /hotels/{hotel_id}/rooms/{room_id}
  - PUT /hotels/{hotel_id}/rooms/{room_id}
  - PATCH /hotels/{hotel_id}/rooms/{room_id}
### Бронирования:
  - GET /bookings
  - POST /bookings
  - GET /bookings/me

## ⚙️ Установка и запуск

```bash
# 1. Клонируем репозиторий
git clone https://github.com/vladikhub/BookingAPI.git

# 2. Устанавливаем зависимости
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt

# 3. Применяем миграции
alembic upgrade head

# 4. Запуск проекта
uvicorn app.main:app --reload
