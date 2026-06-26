import time
import asyncpg

from app.database import get_pool


async def list_tags():
    pool = get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM tags ORDER BY name ASC")
        return [dict(r) for r in rows]


async def get_tag(tag_id: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM tags WHERE id = $1", tag_id)
        return dict(row) if row else None


async def create_tag(data):
    pool = get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO tags (name, created_at)
            VALUES ($1, $2)
            RETURNING *
            """,
            data.name,
            int(time.time()),
        )
        return dict(row)


async def update_tag(tag_id: int, data):
    fields = data.model_dump(exclude_unset=True)
    if not fields:
        return await get_tag(tag_id)

    set_clause = ", ".join(f"{key} = ${i+2}" for i, key in enumerate(fields))
    values = list(fields.values())

    pool = get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            f"UPDATE tags SET {set_clause} WHERE id = $1 RETURNING *",
            tag_id,
            *values,
        )
        return dict(row) if row else None


async def delete_tag(tag_id: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM tags WHERE id = $1", tag_id)
        return result != "DELETE 0"


async def get_tags_for_car(car_id: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT t.* FROM tags t
            JOIN car_tags ct ON ct.tag_id = t.id
            WHERE ct.car_id = $1
            ORDER BY t.name ASC
            """,
            car_id,
        )
        return [dict(r) for r in rows]


async def attach_tag_to_car(car_id: int, tag_id: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        try:
            await conn.execute(
                "INSERT INTO car_tags (car_id, tag_id) VALUES ($1, $2)",
                car_id,
                tag_id,
            )
            return True
        except asyncpg.UniqueViolationError:
            return True
        except asyncpg.ForeignKeyViolationError:
            return False


async def detach_tag_from_car(car_id: int, tag_id: int):
    pool = get_pool()
    async with pool.acquire() as conn:
        result = await conn.execute(
            "DELETE FROM car_tags WHERE car_id = $1 AND tag_id = $2",
            car_id,
            tag_id,
        )
        return result != "DELETE 0"
