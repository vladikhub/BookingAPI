import time

import asyncio
from PIL import Image
import os

from fastapi import BackgroundTasks

from src.database import async_session_maker, async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import BDManager


@celery_instance.task
def test_task():
    time.sleep(5)
    print("Задача выполнена")



def resize_image(input_path: str) -> None:
    output_folder = "src/static/images/"
    target_sizes = [100000, 500, 200]
    with Image.open(input_path) as img:
        # Получаем имя файла без расширения
        filename = os.path.splitext(os.path.basename(input_path))[0]
        extension = os.path.splitext(input_path)[1].lower()

        # Размеры для сохранения

        for size in target_sizes:
            # Вычисляем пропорциональную ширину
            width_percent = (size / float(img.size[0]))
            new_height = int((float(img.size[1]) * float(width_percent)))

            # Изменяем размер
            resized_img = img.resize((size, new_height), Image.LANCZOS)

            # Сохраняем изображение
            output_path = os.path.join(output_folder, f"{filename}_{size}px{extension}")
            resized_img.save(output_path)
    print(f"Изображение сохранено в {output_folder}")


async def get_bookings_with_today_checkin_helper():
    print("Запуск")
    async with BDManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def send_email_to_users_with_today_checkin():
    asyncio.run(get_bookings_with_today_checkin_helper())
