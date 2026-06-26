from fastapi import APIRouter
from fastapi import File
from fastapi import Form
from fastapi import UploadFile

from app.services.image_service import (
    save_image,
    list_images,
    delete_image,
)

router = APIRouter()


@router.post("/api/cars/{car_id}/images")
async def upload_image(
    car_id: str,
    file: UploadFile = File(...),
    image_type: str = Form("gallery"),
):
    return await save_image(
        car_id,
        file,
        image_type,
    )


@router.get("/api/cars/{car_id}/images")
async def get_images(car_id: str):
    return await list_images(car_id)


@router.delete("/api/images/{image_id}")
async def remove_image(image_id: str):
    return await delete_image(image_id)

