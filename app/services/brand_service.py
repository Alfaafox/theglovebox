import time

from fastapi import HTTPException

from app.database import get_pool


async def list_brands():
    pool = get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT *
            FROM brands
            ORDER BY name ASC
            """
        )

    return [dict(r) for r in rows]


async def get_brand(brand_id: int):
    pool = get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT *
            FROM brands
            WHERE id=$1
            """,
            brand_id,
        )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Brand not found",
        )

    return dict(row)


async def create_brand(brand):
    pool = get_pool()

    created_at = int(time.time() * 1000)

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO brands
            (
                name,
                country,
                website,
                logo,
                created_at
            )
            VALUES
            (
                $1,$2,$3,$4,$5
            )
            RETURNING *
            """,
            brand.name,
            brand.country,
            brand.website,
            brand.logo,
            created_at,
        )

    return dict(row)


async def update_brand(
    brand_id: int,
    brand,
):
    pool = get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            UPDATE brands
            SET
                name=$1,
                country=$2,
                website=$3,
                logo=$4
            WHERE id=$5
            RETURNING *
            """,
            brand.name,
            brand.country,
            brand.website,
            brand.logo,
            brand_id,
        )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Brand not found",
        )

    return dict(row)


async def delete_brand(
    brand_id: int,
):
    pool = get_pool()

    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            DELETE
            FROM brands
            WHERE id=$1
            """,
            brand_id,
        )

    if result == "DELETE 0":
        raise HTTPException(
            status_code=404,
            detail="Brand not found",
        )

    return {
        "ok": True
    }

