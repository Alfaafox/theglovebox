from fastapi import APIRouter

from app.schemas.car import (
    CarCreate,
    CarUpdate,
)

from app.services.car_service import (
    list_cars,
    get_car,
    create_car,
    update_car,
    delete_car,
)

router = APIRouter()


@router.get("")
async def get_all_cars():
    return await list_cars()


@router.get("/{car_id}")
async def get_single_car(car_id: str):
    return await get_car(car_id)


@router.post("")
async def add_car(car: CarCreate):
    return await create_car(car)


@router.put("/{car_id}")
async def edit_car(
    car_id: str,
    car: CarUpdate,
):
    return await update_car(car_id, car)


@router.delete("/{car_id}")
async def remove_car(car_id: str):
    return await delete_car(car_id)

