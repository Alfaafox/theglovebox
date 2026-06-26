import time

from fastapi import HTTPException

from app.database import get_pool


async def list_manufacturers():

    pool = get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT *
            FROM manufacturers
            ORDER BY name
            """
        )

    return [dict(r) for r in rows]


async def get_manufacturer(manufacturer_id: int):

    pool = get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT *
            FROM manufacturers
            WHERE id=$1
            """,
            manufacturer_id,
        )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Manufacturer not found",
        )

    return dict(row)


async def create_manufacturer(manufacturer):

    pool = get_pool()

    created_at = int(time.time() * 1000)

    async with pool.acquire() as conn:

        row = await conn.fetchrow(
            """
            INSERT INTO manufacturers
            (
                name,
                country,
                website,
                logo,
                created_at
            )
            VALUES
            ($1,$2,$3,$4,$5)
            RETURNING *
            """,
            manufacturer.name,
            manufacturer.country,
            manufacturer.website,
            manufacturer.logo,
            created_at,
        )

    return dict(row)


async def update_manufacturer(
    manufacturer_id,
    manufacturer,
):

    pool = get_pool()

    async with pool.acquire() as conn:

        row = await conn.fetchrow(
            """
            UPDATE manufacturers
            SET
                name=$1,
                country=$2,
                website=$3,
                logo=$4
            WHERE id=$5
            RETURNING *
            """,
            manufacturer.name,
            manufacturer.country,
            manufacturer.website,
            manufacturer.logo,
            manufacturer_id,
        )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Manufacturer not found",
        )

    return dict(row)


async def delete_manufacturer(manufacturer_id):

    pool = get_pool()

    async with pool.acquire() as conn:

        result = await conn.execute(
            """
            DELETE
            FROM manufacturers
            WHERE id=$1
            """,
            manufacturer_id,
        )

    if result == "DELETE 0":
        raise HTTPException(
            status_code=404,
            detail="Manufacturer not found",
        )

    return {
        "ok": True
    }

