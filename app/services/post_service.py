import time
import uuid

from fastapi import HTTPException

from app.database import get_pool


async def list_posts():
    pool = get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """
            SELECT *
            FROM posts
            ORDER BY created_at DESC
            """
        )

    return [dict(row) for row in rows]


async def get_post(post_id: str):
    pool = get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT *
            FROM posts
            WHERE id=$1
            """,
            post_id,
        )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return dict(row)


async def create_post(post):
    pool = get_pool()

    post_id = str(uuid.uuid4())
    created_at = int(time.time() * 1000)

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO posts
            (
                id,
                title,
                body,
                created_at
            )
            VALUES
            (
                $1,$2,$3,$4
            )
            """,
            post_id,
            post.title,
            post.body,
            created_at,
        )

    return {
        "id": post_id,
        **post.model_dump(),
        "created_at": created_at,
    }


async def update_post(post_id: str, post):
    pool = get_pool()

    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            UPDATE posts
            SET
                title=$1,
                body=$2
            WHERE id=$3
            """,
            post.title,
            post.body,
            post_id,
        )

    if result == "UPDATE 0":
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return {
        "id": post_id,
        **post.model_dump(),
    }


async def delete_post(post_id: str):
    pool = get_pool()

    async with pool.acquire() as conn:
        result = await conn.execute(
            """
            DELETE FROM posts
            WHERE id=$1
            """,
            post_id,
        )

    if result == "DELETE 0":
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return {
        "ok": True,
    }

