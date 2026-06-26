from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME
from app.config import UPLOAD_DIR

from app.database import (
    connect,
    disconnect,
    initialize_database,
)

from app.routers.cars import router as cars_router
from app.routers.posts import router as posts_router
from app.routers.health import router as health_router
from app.routers.upload import router as upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    await connect()
    await initialize_database()

    yield

    await disconnect()


app = FastAPI(
    title=APP_NAME,
    version="2.1.0",
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

app.include_router(
    health_router,
    tags=["Health"],
)

app.include_router(
    cars_router,
    prefix="/api/cars",
    tags=["Garage"],
)

app.include_router(
    posts_router,
    prefix="/api/posts",
    tags=["Blog"],
)

app.include_router(
    upload_router,
    tags=["Images"],
)


@app.get("/")
async def root():

    return {
        "application": APP_NAME,
        "version": "2.1.0",
        "status": "running",
    }

