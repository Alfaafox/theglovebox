import asyncpg

from app.config import DATABASE_URL

pool = None


async def connect():
    """
    Create PostgreSQL connection pool.
    """
    global pool

    if pool is None:
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=5,
        )


async def disconnect():
    """
    Close PostgreSQL connection pool.
    """
    global pool

    if pool:
        await pool.close()
        pool = None


def get_pool():
    if pool is None:
        raise RuntimeError("Database has not been initialized.")
    return pool


async def initialize_database():
    """
    Create application tables if they don't exist.
    """

    async with pool.acquire() as conn:

        # ---------------------------------------------------------------------
        # Cars
        # ---------------------------------------------------------------------

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cars (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                brand TEXT,
                status TEXT DEFAULT 'owned',
                variant TEXT,
                tags TEXT[],
                photo TEXT,
                story TEXT,
                created_at BIGINT
            );
            """
        )

        # ---------------------------------------------------------------------
        # Blog Posts
        # ---------------------------------------------------------------------

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at BIGINT
            );
            """
        )

