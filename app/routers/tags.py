from fastapi import APIRouter, HTTPException, Depends

from app.schemas.tag import TagCreate, TagUpdate
from app.services import tag_service
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("")
async def get_all_tags():
    return await tag_service.list_tags()


@router.get("/{tag_id}")
async def get_single_tag(tag_id: int):
    tag = await tag_service.get_tag(tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("")
async def add_tag(data: TagCreate, current_user: dict = Depends(get_current_user)):
    return await tag_service.create_tag(data)


@router.put("/{tag_id}")
async def edit_tag(
    tag_id: int,
    data: TagUpdate,
    current_user: dict = Depends(get_current_user),
):
    updated = await tag_service.update_tag(tag_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated


@router.delete("/{tag_id}")
async def remove_tag(tag_id: int, current_user: dict = Depends(get_current_user)):
    deleted = await tag_service.delete_tag(tag_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted"}
