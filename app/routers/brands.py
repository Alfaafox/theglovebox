from fastapi import APIRouter, Depends

from app.schemas.brand import (
    BrandCreate,
    BrandUpdate,
)
from app.services.brand_service import (
    list_brands,
    get_brand,
    create_brand,
    update_brand,
    delete_brand,
)
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("")
async def get_all_brands():
    return await list_brands()


@router.get("/{brand_id}")
async def get_single_brand(brand_id: int):
    return await get_brand(brand_id)


@router.post("")
async def add_brand(brand: BrandCreate, current_user: dict = Depends(get_current_user)):
    return await create_brand(brand)


@router.put("/{brand_id}")
async def edit_brand(
    brand_id: int,
    brand: BrandUpdate,
    current_user: dict = Depends(get_current_user),
):
    return await update_brand(brand_id, brand)


@router.delete("/{brand_id}")
async def remove_brand(brand_id: int, current_user: dict = Depends(get_current_user)):
    return await delete_brand(brand_id)
