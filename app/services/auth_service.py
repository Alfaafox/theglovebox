import time
import bcrypt
import jwt

from fastapi import HTTPException, Header

from app.database import get_pool
from app.config import SECRET_KEY

JWT_ALGORITHM = "HS256"
JWT_EXPIRY_SECONDS = 60 * 60 * 24  # 24 hours


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def _create_token(user_id: int, username: str) -> str:
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": int(time.time()) + JWT_EXPIRY_SECONDS,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


async def register_user(username: str, password: str):
    pool = get_pool()
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT id FROM users WHERE username = $1", username
        )
        if existing:
            raise HTTPException(status_code=409, detail="Username already taken")

        password_hash = _hash_password(password)
        created_at = int(time.time() * 1000)

        row = await conn.fetchrow(
            """
            INSERT INTO users (username, password_hash, created_at)
            VALUES ($1, $2, $3)
            RETURNING id, username, created_at
            """,
            username,
            password_hash,
            created_at,
        )
        return dict(row)


async def login_user(username: str, password: str):
    pool = get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE username = $1", username
        )

    if not row or not _verify_password(password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = _create_token(row["id"], row["username"])
    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload["sub"])

    pool = get_pool()
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT id, username, created_at FROM users WHERE id = $1", user_id
        )

    if not row:
        raise HTTPException(status_code=401, detail="User no longer exists")

    return dict(row)
