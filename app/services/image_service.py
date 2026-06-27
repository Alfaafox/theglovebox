import os
import time
import uuid
import io
from typing import List

from fastapi import HTTPException, UploadFile
from PIL import Image

from app.database import get_pool
from app.config import CAR_UPLOAD_DIR

ALLOWED = {".jpg", ".jpeg", ".png", ".webp"}

MAIN_MAX_DIMENSION = 1920
THUMB_MAX_DIMENSION = 400


def _car_folder(car_id: int):
    folder = CAR_UPLOAD_DIR / str(car_id)
    folder.mkdir(parents=True, exist_ok=True)
    return folder


async def _car_exists(conn, car_id: int) -> bool:
    row = await conn.fetchrow("SELECT id FROM cars WHERE id = $1", car_id)
    return row is not None


def _process_and_save(folder, contents: bytes):
    image = Image.open(io.BytesIO(contents))
    image = image.convert("RGB")

    unique_id = uuid.uuid4().hex
    filename = f"{unique_id}.webp"
    thumb_filename = f"{unique_id}_thumb.webp"

    main_img = image.copy()
    main_img.thumbnail((MAIN_MAX_DIMENSION, MAIN_MAX_DIMENSION))
    main_img.save(folder / filename, "WEBP", quality=85)

    thumb_img = image.copy()
    thumb_img.thumbnail((THUMB_MAX_DIMENSION, THUMB_MAX_DIMENSION))
    thumb_img.save(folder / thumb_filename, "WEBP", quality=80)

    return filename, thumb_filename


async def save_images(
    car_id: int,
    files: List[UploadFile],
    image_type: str = "gallery",
):
    pool = get_pool()

    async with pool.acquire() as conn:
        if not await _car_exists(conn, car_id):
            raise HTTPException(status_code=404, detail="Car not found")

        existing = await conn.fetch(
            "SELECT is_primary FROM car_images WHERE car_id = $1",
            car_id,
        )
        has_primary = any(r["is_primary"] for r in existing)
        next_order = len(existing)

        folder = _car_folder(car_id)
        created = []

        for file in files:
            extension = os.path.splitext(file.filename or "")[1].lower()
            if extension not in ALLOWED:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported image format: {file.filename}",
                )

            contents = await file.read()

            try:
                filename, thumb_filename = _process_and_save(folder, contents)
            except HTTPException:
                raise
            except Exception:
                raise HTTPException(
                    status_code=400,
                    detail=f"Could not process image: {file.filename}",
                )

            is_primary = not has_primary
            if is_primary:
                has_primary = True

            created_at = int(time.time() * 1000)

            row = await conn.fetchrow(
                """
                INSERT INTO car_images
                (car_id, filename, original_name, image_type, display_order, is_primary, created_at)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING *
                """,
                car_id,
                filename,
                file.filename,
                image_type,
                next_order,
                is_primary,
                created_at,
            )

            record = dict(row)
            record["thumbnail_filename"] = thumb_filename
            created.append(record)
            next_order += 1

    return created


async def list_images(car_id: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT * FROM car_images
            WHERE car_id = $1
            ORDER BY display_order, created_at
            """,
            car_id,
        )

    results = []
    for r in rows:
        record = dict(r)
        base = os.path.splitext(record["filename"])[0]
        record["thumbnail_filename"] = f"{base}_thumb.webp"
        results.append(record)
    return results


async def delete_image(image_id: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM car_images WHERE id = $1",
            image_id,
        )
        if row is None:
            raise HTTPException(status_code=404, detail="Image not found")

        await conn.execute("DELETE FROM car_images WHERE id = $1", image_id)

        if row["is_primary"]:
            next_image = await conn.fetchrow(
                """
                SELECT id FROM car_images
                WHERE car_id = $1
                ORDER BY display_order, created_at
                LIMIT 1
                """,
                row["car_id"],
            )
            if next_image:
                await conn.execute(
                    "UPDATE car_images SET is_primary = TRUE WHERE id = $1",
                    next_image["id"],
                )

    folder = CAR_UPLOAD_DIR / str(row["car_id"])
    base = os.path.splitext(row["filename"])[0]
    thumb_filename = f"{base}_thumb.webp"

    main_path = folder / row["filename"]
    thumb_path = folder / thumb_filename

    if main_path.exists():
        main_path.unlink()
    if thumb_path.exists():
        thumb_path.unlink()

    return {"ok": True}


async def set_primary_image(car_id: int, image_id: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        target = await conn.fetchrow(
            "SELECT * FROM car_images WHERE id = $1 AND car_id = $2",
            image_id,
            car_id,
        )
        if target is None:
            raise HTTPException(
                status_code=404, detail="Image not found for this car"
            )

        await conn.execute(
            "UPDATE car_images SET is_primary = FALSE WHERE car_id = $1",
            car_id,
        )
        row = await conn.fetchrow(
            "UPDATE car_images SET is_primary = TRUE WHERE id = $1 RETURNING *",
            image_id,
        )

    return dict(row)
