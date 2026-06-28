from fastapi import APIRouter, HTTPException, Depends

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

from app.schemas.tag import CarTagAttach
from app.services import tag_service
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("")
async def get_all_cars():
    return await list_cars()


@router.get("/{car_id}")
async def get_single_car(car_id: int):
    return await get_car(car_id)


@router.post("")
async def add_car(data: CarCreate, current_user: dict = Depends(get_current_user)):
    return await create_car(data)


@router.put("/{car_id}")
async def edit_car(
    car_id: int,
    data: CarUpdate,
    current_user: dict = Depends(get_current_user),
):
    return await update_car(car_id, data)


@router.delete("/{car_id}")
async def remove_car(car_id: int, current_user: dict = Depends(get_current_user)):
    return await delete_car(car_id)


@router.get("/{car_id}/tags")
async def list_car_tags(car_id: int):
    return await tag_service.get_tags_for_car(car_id)


@router.post("/{car_id}/tags", status_code=201)
async def attach_tag(
    car_id: int,
    payload: CarTagAttach,
    current_user: dict = Depends(get_current_user),
):
    success = await tag_service.attach_tag_to_car(car_id, payload.tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Car or tag not found")
    return {"message": "Tag attached"}


@router.delete("/{car_id}/tags/{tag_id}", status_code=204)
async def detach_tag(
    car_id: int,
    tag_id: int,
    current_user: dict = Depends(get_current_user),
):
    success = await tag_service.detach_tag_from_car(car_id, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not attached to this car")
