from fastapi import APIRouter

from app.schemas.series import (
    SeriesCreate,
    SeriesUpdate,
)

from app.services.series_service import (
    list_series,
    get_series,
    create_series,
    update_series,
    delete_series,
)

router = APIRouter()


@router.get("")
async def get_all():
    return await list_series()


@router.get("/{series_id}")
async def get_one(series_id: int):
    return await get_series(series_id)


@router.post("")
async def create(data: SeriesCreate):
    return await create_series(data)


@router.put("/{series_id}")
async def update(series_id: int, data: SeriesUpdate):
    return await update_series(series_id, data)


@router.delete("/{series_id}")
async def delete(series_id: int):
    return await delete_series(series_id)
