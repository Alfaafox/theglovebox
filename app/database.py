import asyncpg

from app.config import DATABASE_URL

pool = None


async def connect():
    global pool

    if pool is None:
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=1,
            max_size=5,
        )


async def disconnect():
    global pool

    if pool:
        await pool.close()
        pool = None


def get_pool():
    return pool


async def initialize_database():

    async with pool.acquire() as conn:

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS brands(
            id BIGSERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            country TEXT,
            website TEXT,
            logo TEXT,
            created_at BIGINT NOT NULL
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS manufacturers(
            id BIGSERIAL PRIMARY KEY,
            name TEXT UNIQUE NOT NULL,
            country TEXT,
            website TEXT,
            logo TEXT,
            created_at BIGINT NOT NULL
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS series(
            id BIGSERIAL PRIMARY KEY,
            brand_id BIGINT NOT NULL REFERENCES brands(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            description TEXT,
            created_at BIGINT NOT NULL
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS cars(
            id BIGSERIAL PRIMARY KEY,

            brand_id BIGINT NOT NULL REFERENCES brands(id),
            manufacturer_id BIGINT NOT NULL REFERENCES manufacturers(id),
            series_id BIGINT NOT NULL REFERENCES series(id),

            name TEXT NOT NULL,
            variant TEXT,
            scale TEXT,
            year INTEGER,
            country TEXT,

            status TEXT DEFAULT 'owned',

            purchase_price NUMERIC(12,2),
            purchase_date DATE,
            purchase_location TEXT,

            estimated_value NUMERIC(12,2),

            story TEXT,
            notes TEXT,

            created_at BIGINT NOT NULL,
            updated_at BIGINT NOT NULL
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS car_images(
            id BIGSERIAL PRIMARY KEY,

            car_id BIGINT NOT NULL REFERENCES cars(id) ON DELETE CASCADE,

            filename TEXT NOT NULL,
            original_name TEXT,

            image_type TEXT,

            display_order INTEGER DEFAULT 0,

            is_primary BOOLEAN DEFAULT FALSE,

            created_at BIGINT NOT NULL
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS tags(
            id BIGSERIAL PRIMARY KEY,

            name TEXT UNIQUE NOT NULL,

            created_at BIGINT NOT NULL
        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS car_tags(

            car_id BIGINT NOT NULL REFERENCES cars(id) ON DELETE CASCADE,

            tag_id BIGINT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,

            PRIMARY KEY(car_id,tag_id)

        );
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS posts(

            id BIGSERIAL PRIMARY KEY,

            title TEXT NOT NULL,

            body TEXT NOT NULL,

            created_at BIGINT NOT NULL

        );
        """)

        await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_brand
        ON cars(brand_id);
        """)

        await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_manufacturer
        ON cars(manufacturer_id);
        """)

        await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_series
        ON cars(series_id);
        """)

        await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_status
        ON cars(status);
        """)

        await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_car_images
        ON car_images(car_id);
        """)

        await conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_tags
        ON car_tags(car_id);
        """)
