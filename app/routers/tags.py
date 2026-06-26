from fastapi import APIRouter, HTTPException

from app.schemas.tag import TagCreate, TagUpdate

from app.services import tag_service

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
async def add_tag(data: TagCreate):
    return await tag_service.create_tag(data)


@router.put("/{tag_id}")
async def edit_tag(tag_id: int, data: TagUpdate):
    updated = await tag_service.update_tag(tag_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Tag not found")
    return updated


@router.delete("/{tag_id}")
async def remove_tag(tag_id: int):
    deleted = await tag_service.delete_tag(tag_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted"}
