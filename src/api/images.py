from fastapi import APIRouter, UploadFile, BackgroundTasks
import shutil

from src.services.images import ImageService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("")
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImageService().upload_image(file, background_tasks)
