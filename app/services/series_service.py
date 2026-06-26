import time

from fastapi import HTTPException

from app.database import get_pool


async def list_series():

    pool = get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT
                s.*,
                b.name AS brand_name
            FROM series s
            JOIN brands b
              ON b.id=s.brand_id
            ORDER BY b.name,s.name
            """
        )

    return [dict(r) for r in rows]


async def get_series(series_id:int):

    pool=get_pool()

    async with pool.acquire() as conn:

        row=await conn.fetchrow(
            """
            SELECT *
            FROM series
            WHERE id=$1
            """,
            series_id
        )

    if row is None:
        raise HTTPException(404,"Series not found")

    return dict(row)


async def create_series(data):

    pool=get_pool()

    created_at=int(time.time()*1000)

    async with pool.acquire() as conn:

        row=await conn.fetchrow(
            """
            INSERT INTO series
            (
                brand_id,
                name,
                description,
                created_at
            )
            VALUES
            ($1,$2,$3,$4)
            RETURNING *
            """,
            data.brand_id,
            data.name,
            data.description,
            created_at
        )

    return dict(row)


async def update_series(series_id,data):

    pool=get_pool()

    async with pool.acquire() as conn:

        row=await conn.fetchrow(
            """
            UPDATE series
            SET
                brand_id=$1,
                name=$2,
                description=$3
            WHERE id=$4
            RETURNING *
            """,
            data.brand_id,
            data.name,
            data.description,
            series_id
        )

    if row is None:
        raise HTTPException(404,"Series not found")

    return dict(row)


async def delete_series(series_id):

    pool=get_pool()

    async with pool.acquire() as conn:

        result=await conn.execute(
            """
            DELETE FROM series
            WHERE id=$1
            """,
            series_id
        )

    if result=="DELETE 0":
        raise HTTPException(404,"Series not found")

    return {"ok":True}

