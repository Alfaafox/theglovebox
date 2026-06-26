from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncpg
import os
import uuid
import time

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://siteuser:sitepass@localhost:5432/sitedb")

app = FastAPI(title="Collection Site API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pool = None


@app.on_event("startup")
async def startup():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)
    async with pool.acquire() as conn:
        await conn.execute("""
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
        """)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at BIGINT
            );
        """)


@app.on_event("shutdown")
async def shutdown():
    if pool:
        await pool.close()


class CarIn(BaseModel):
    name: str
    brand: Optional[str] = ""
    status: Optional[str] = "owned"
    variant: Optional[str] = ""
    tags: Optional[List[str]] = []
    photo: Optional[str] = ""
    story: Optional[str] = ""


class PostIn(BaseModel):
    title: str
    body: str


@app.get("/api/cars")
async def list_cars():
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM cars ORDER BY created_at DESC")
        return [dict(r) for r in rows]


@app.post("/api/cars")
async def create_car(car: CarIn):
    car_id = str(uuid.uuid4())
    created_at = int(time.time() * 1000)
    async with pool.acquire() as conn:
        await conn.execute(
            """INSERT INTO cars (id, name, brand, status, variant, tags, photo, story, created_at)
               VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)""",
            car_id, car.name, car.brand, car.status, car.variant,
            car.tags, car.photo, car.story, created_at
        )
    return {"id": car_id, **car.dict(), "created_at": created_at}


@app.put("/api/cars/{car_id}")
async def update_car(car_id: str, car: CarIn):
    async with pool.acquire() as conn:
        result = await conn.execute(
            """UPDATE cars SET name=$1, brand=$2, status=$3, variant=$4, tags=$5, photo=$6, story=$7
               WHERE id=$8""",
            car.name, car.brand, car.status, car.variant, car.tags, car.photo, car.story, car_id
        )
        if result == "UPDATE 0":
            raise HTTPException(status_code=404, detail="Car not found")
    return {"id": car_id, **car.dict()}


@app.delete("/api/cars/{car_id}")
async def delete_car(car_id: str):
    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM cars WHERE id=$1", car_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Car not found")
    return {"ok": True}


@app.get("/api/posts")
async def list_posts():
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM posts ORDER BY created_at DESC")
        return [dict(r) for r in rows]


@app.post("/api/posts")
async def create_post(post: PostIn):
    post_id = str(uuid.uuid4())
    created_at = int(time.time() * 1000)
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO posts (id, title, body, created_at) VALUES ($1,$2,$3,$4)",
            post_id, post.title, post.body, created_at
        )
    return {"id": post_id, "title": post.title, "body": post.body, "created_at": created_at}


@app.put("/api/posts/{post_id}")
async def update_post(post_id: str, post: PostIn):
    async with pool.acquire() as conn:
        result = await conn.execute(
            "UPDATE posts SET title=$1, body=$2 WHERE id=$3",
            post.title, post.body, post_id
        )
        if result == "UPDATE 0":
            raise HTTPException(status_code=404, detail="Post not found")
    return {"id": post_id, "title": post.title, "body": post.body}


@app.delete("/api/posts/{post_id}")
async def delete_post(post_id: str):
    async with pool.acquire() as conn:
        result = await conn.execute("DELETE FROM posts WHERE id=$1", post_id)
        if result == "DELETE 0":
            raise HTTPException(status_code=404, detail="Post not found")
    return {"ok": True}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
