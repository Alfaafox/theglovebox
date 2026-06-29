import time

from fastapi import HTTPException

from app.database import get_pool


async def list_cars(
    q: str = None,
    brand_id: int = None,
    manufacturer_id: int = None,
    series_id: int = None,
    status: str = None,
    tag_id: int = None,
):

    pool = get_pool()

    conditions = []
    params = []

    def add_param(value):
        params.append(value)
        return f"${len(params)}"

    if q:
        placeholder = add_param(f"%{q}%")
        conditions.append(
            f"(c.name ILIKE {placeholder} OR c.variant ILIKE {placeholder})"
        )

    if brand_id is not None:
        conditions.append(f"c.brand_id = {add_param(brand_id)}")

    if manufacturer_id is not None:
        conditions.append(f"c.manufacturer_id = {add_param(manufacturer_id)}")

    if series_id is not None:
        conditions.append(f"c.series_id = {add_param(series_id)}")

    if status:
        conditions.append(f"c.status = {add_param(status)}")

    tag_join = ""
    if tag_id is not None:
        tag_join = "INNER JOIN car_tags ct ON ct.car_id = c.id"
        conditions.append(f"ct.tag_id = {add_param(tag_id)}")

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query = f"""
        SELECT
            c.id,
            c.name,
            c.variant,
            c.scale,
            c.year,
            c.country,
            c.status,
            c.purchase_price,
            c.purchase_date,
            c.purchase_location,
            c.estimated_value,
            c.story,
            c.notes,
            c.created_at,
            c.updated_at,

            b.id   AS brand_id,
            b.name AS brand,

            m.id   AS manufacturer_id,
            m.name AS manufacturer,

            s.id   AS series_id,
            s.name AS series

        FROM cars c

        INNER JOIN brands b
            ON b.id=c.brand_id

        INNER JOIN manufacturers m
            ON m.id=c.manufacturer_id

        INNER JOIN series s
            ON s.id=c.series_id

        {tag_join}

        {where_clause}

        ORDER BY c.created_at DESC
    """

    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)

    return [dict(r) for r in rows]


async def get_car(car_id: int):

    pool = get_pool()

    async with pool.acquire() as conn:

        row = await conn.fetchrow(
            """
            SELECT
                c.*,

                b.name AS brand,
                m.name AS manufacturer,
                s.name AS series

            FROM cars c

            INNER JOIN brands b
                ON b.id=c.brand_id

            INNER JOIN manufacturers m
                ON m.id=c.manufacturer_id

            INNER JOIN series s
                ON s.id=c.series_id

            WHERE c.id=$1
            """,
            car_id,
        )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Car not found",
        )

    return dict(row)


async def create_car(data):

    pool = get_pool()

    now = int(time.time() * 1000)

    async with pool.acquire() as conn:

        brand = await conn.fetchval(
            "SELECT id FROM brands WHERE id=$1",
            data.brand_id,
        )

        if brand is None:
            raise HTTPException(
                400,
                "Invalid brand.",
            )

        manufacturer = await conn.fetchval(
            "SELECT id FROM manufacturers WHERE id=$1",
            data.manufacturer_id,
        )

        if manufacturer is None:
            raise HTTPException(
                400,
                "Invalid manufacturer.",
            )

        series = await conn.fetchval(
            "SELECT id FROM series WHERE id=$1",
            data.series_id,
        )

        if series is None:
            raise HTTPException(
                400,
                "Invalid series.",
            )

        row = await conn.fetchrow(
            """
            INSERT INTO cars
            (
                brand_id,
                manufacturer_id,
                series_id,

                name,
                variant,
                scale,
                year,
                country,

                status,

                purchase_price,
                purchase_date,
                purchase_location,

                estimated_value,

                story,
                notes,

                created_at,
                updated_at

            )
            VALUES
            (
                $1,$2,$3,
                $4,$5,$6,$7,$8,
                $9,
                $10,$11,$12,
                $13,
                $14,$15,
                $16,$17
            )
            RETURNING *
            """,
            data.brand_id,
            data.manufacturer_id,
            data.series_id,

            data.name,
            data.variant,
            data.scale,
            data.year,
            data.country,

            data.status,

            data.purchase_price,
            data.purchase_date,
            data.purchase_location,

            data.estimated_value,

            data.story,
            data.notes,

            now,
            now,
        )

    return dict(row)


async def update_car(car_id: int, data):

    pool = get_pool()

    now = int(time.time() * 1000)

    async with pool.acquire() as conn:

        row = await conn.fetchrow(
            """
            UPDATE cars
            SET

                brand_id=$1,
                manufacturer_id=$2,
                series_id=$3,

                name=$4,
                variant=$5,
                scale=$6,
                year=$7,
                country=$8,

                status=$9,

                purchase_price=$10,
                purchase_date=$11,
                purchase_location=$12,

                estimated_value=$13,

                story=$14,
                notes=$15,

                updated_at=$16

            WHERE id=$17

            RETURNING *
            """,
            data.brand_id,
            data.manufacturer_id,
            data.series_id,

            data.name,
            data.variant,
            data.scale,
            data.year,
            data.country,

            data.status,

            data.purchase_price,
            data.purchase_date,
            data.purchase_location,

            data.estimated_value,

            data.story,
            data.notes,

            now,

            car_id,
        )

    if row is None:
        raise HTTPException(
            404,
            "Car not found",
        )

    return dict(row)


async def delete_car(car_id: int):

    pool = get_pool()

    async with pool.acquire() as conn:

        result = await conn.execute(
            """
            DELETE
            FROM cars
            WHERE id=$1
            """,
            car_id,
        )

    if result == "DELETE 0":
        raise HTTPException(
            404,
            "Car not found",
        )

    return {
        "ok": True
    }
