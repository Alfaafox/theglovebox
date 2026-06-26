from fastapi import APIRouter

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

router = APIRouter()


@router.get("")
async def get_all():
    return await list_manufacturers()


@router.get("/{manufacturer_id}")
async def get_one(manufacturer_id: int):
    return await get_manufacturer(manufacturer_id)


@router.post("")
async def create(data: ManufacturerCreate):
    return await create_manufacturer(data)


@router.put("/{manufacturer_id}")
async def update(
    manufacturer_id: int,
    data: ManufacturerUpdate,
):
    return await update_manufacturer(
        manufacturer_id,
        data,
    )


@router.delete("/{manufacturer_id}")
async def delete(manufacturer_id: int):
    return await delete_manufacturer(manufacturer_id)

