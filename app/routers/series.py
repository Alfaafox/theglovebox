from fastapi import APIRouter, Depends

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
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("")
async def get_all():
    return await list_series()


@router.get("/{series_id}")
async def get_one(series_id: int):
    return await get_series(series_id)


@router.post("")
async def create(data: SeriesCreate, current_user: dict = Depends(get_current_user)):
    return await create_series(data)


@router.put("/{series_id}")
async def update(
    series_id: int,
    data: SeriesUpdate,
    current_user: dict = Depends(get_current_user),
):
    return await update_series(series_id, data)


@router.delete("/{series_id}")
async def delete(series_id: int, current_user: dict = Depends(get_current_user)):
    return await delete_series(series_id)
