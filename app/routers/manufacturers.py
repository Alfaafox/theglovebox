from fastapi import APIRouter, Depends

from app.schemas.manufacturer import (
    ManufacturerCreate,
    ManufacturerUpdate,
)
from app.services.manufacturer_service import (
    list_manufacturers,
    get_manufacturer,
    create_manufacturer,
    update_manufacturer,
    delete_manufacturer,
)
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("")
async def get_all():
    return await list_manufacturers()


@router.get("/{manufacturer_id}")
async def get_one(manufacturer_id: int):
    return await get_manufacturer(manufacturer_id)


@router.post("")
async def create(data: ManufacturerCreate, current_user: dict = Depends(get_current_user)):
    return await create_manufacturer(data)


@router.put("/{manufacturer_id}")
async def update(
    manufacturer_id: int,
    data: ManufacturerUpdate,
    current_user: dict = Depends(get_current_user),
):
    return await update_manufacturer(manufacturer_id, data)


@router.delete("/{manufacturer_id}")
async def delete(manufacturer_id: int, current_user: dict = Depends(get_current_user)):
    return await delete_manufacturer(manufacturer_id)
