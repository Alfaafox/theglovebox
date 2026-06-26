import os
import time
import uuid
import shutil

from fastapi import HTTPException, UploadFile

from app.database import get_pool
from app.config import CAR_UPLOAD_DIR


ALLOWED = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


async def save_image(
    car_id: str,
    file: UploadFile,
    image_type: str = "gallery"
):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED:
        raise HTTPException(
            status_code=400,
            detail="Unsupported image format"
        )

    image_id = str(uuid.uuid4())

    folder = CAR_UPLOAD_DIR / car_id
    folder.mkdir(parents=True, exist_ok=True)

    filename = f"{image_id}{extension}"

    destination = folder / filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    created_at = int(time.time() * 1000)

    pool = get_pool()

    async with pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO car_images
            (
                id,
                car_id,
                filename,
                original_name,
                image_type,
                created_at
            )
            VALUES
            ($1,$2,$3,$4,$5,$6)
            """,
            image_id,
            car_id,
            filename,
            file.filename,
            image_type,
            created_at
        )

    return {
        "id": image_id,
        "filename": filename,
        "car_id": car_id
    }


async def list_images(car_id: str):

    pool = get_pool()

    async with pool.acquire() as conn:

        rows = await conn.fetch(
            """
            SELECT *
            FROM car_images
            WHERE car_id=$1
            ORDER BY display_order,
                     created_at
            """,
            car_id
        )

    return [dict(r) for r in rows]


async def delete_image(image_id: str):

    pool = get_pool()

    async with pool.acquire() as conn:

        row = await conn.fetchrow(
            """
            SELECT *
            FROM car_images
            WHERE id=$1
            """,
            image_id
        )

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Image not found"
            )

        await conn.execute(
            """
            DELETE
            FROM car_images
            WHERE id=$1
            """,
            image_id
        )

    path = CAR_UPLOAD_DIR / row["car_id"] / row["filename"]

    if path.exists():
        path.unlink()

    return {
        "ok": True
    }

