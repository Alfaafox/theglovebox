from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME, UPLOAD_DIR

from app.database import (
    connect,
    disconnect,
    initialize_database,
)

from app.routers.health import router as health_router
from app.routers.brands import router as brands_router
from app.routers.manufacturers import router as manufacturers_router
from app.routers.series import router as series_router
from app.routers.cars import router as cars_router
from app.routers.tags import router as tags_router
from app.routers.posts import router as posts_router
from app.routers.upload import router as upload_router
from app.routers.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await connect()
    await initialize_database()

    yield

    await disconnect()


app = FastAPI(
    title=APP_NAME,
    version="3.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOAD_DIR)),
    name="uploads",
)

app.include_router(health_router, tags=["Health"])

app.include_router(brands_router, prefix="/api/brands", tags=["Brands"])

app.include_router(
    manufacturers_router,
    prefix="/api/manufacturers",
    tags=["Manufacturers"],
)

app.include_router(
    series_router,
    prefix="/api/series",
    tags=["Series"],
)

app.include_router(
    cars_router,
    prefix="/api/cars",
    tags=["Cars"],
)

app.include_router(
    tags_router,
    prefix="/api/tags",
    tags=["Tags"],
)

app.include_router(
    posts_router,
    prefix="/api/posts",
    tags=["Posts"],
)

app.include_router(
    upload_router,
    tags=["Images"],
)


@app.get("/")
async def root():
    return {
        "application": APP_NAME,
        "version": "3.0.0",
        "status": "running",
    }


app.include_router(
    auth_router,
    tags=["Auth"],
)
