import time
import uuid

from fastapi import HTTPException

from app.database import get_pool


async def list_cars():
    pool = get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT *
            FROM cars
            ORDER BY created_at DESC
            """
        )

    return [dict(row) for row in rows]


async def get_car(car_id: str):
    pool = get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT *
            FROM cars
            WHERE id=$1
            """,
            car_id,
        )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found",
        )

    return dict(row)


async def create_car(car):
    pool = get_pool()

    car_id = str(uuid.uuid4())
    created_at = int(time.time() * 1000)

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO cars
            (
                id,
                name,
                brand,
                status,
                variant,
                tags,
                photo,
                story,
                created_at
            )
            VALUES
            (
                $1,$2,$3,$4,$5,$6,$7,$8,$9
            )
            """,
            car_id,
            car.name,
            car.brand,
            car.status,
            car.variant,
            car.tags,
            car.photo,
            car.story,
            created_at,
        )

    return {
        "id": car_id,
        **car.model_dump(),
        "created_at": created_at,
    }


async def update_car(car_id: str, car):
    pool = get_pool()

    async with pool.acquire() as conn:

        result = await conn.execute(
            """
            UPDATE cars
            SET
                name=$1,
                brand=$2,
                status=$3,
                variant=$4,
                tags=$5,
                photo=$6,
                story=$7
            WHERE id=$8
            """,
            car.name,
            car.brand,
            car.status,
            car.variant,
            car.tags,
            car.photo,
            car.story,
            car_id,
        )

    if result == "UPDATE 0":
        raise HTTPException(
            status_code=404,
            detail="Car not found",
        )

    return {
        "id": car_id,
        **car.model_dump(),
    }


async def delete_car(car_id: str):
    pool = get_pool()

    async with pool.acquire() as conn:

        result = await conn.execute(
            """
            DELETE FROM cars
            WHERE id=$1
            """,
            car_id,
        )

    if result == "DELETE 0":
        raise HTTPException(
            status_code=404,
            detail="Car not found",
        )

    return {
        "ok": True
    }

