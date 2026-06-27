from typing import List

from fastapi import APIRouter, File, Form, UploadFile

from app.services.image_service import (
    save_images,
    list_images,
    delete_image,
    set_primary_image,
)

router = APIRouter()


@router.post("/api/cars/{car_id}/images")
async def upload_images(
    car_id: int,
    files: List[UploadFile] = File(...),
    image_type: str = Form("gallery"),
):
    return await save_images(car_id, files, image_type)


@router.get("/api/cars/{car_id}/images")
async def get_images(car_id: int):
    return await list_images(car_id)


@router.delete("/api/images/{image_id}")
async def remove_image(image_id: int):
    return await delete_image(image_id)


@router.put("/api/cars/{car_id}/images/{image_id}/primary")
async def make_primary(car_id: int, image_id: int):
    return await set_primary_image(car_id, image_id)
