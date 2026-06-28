from fastapi import APIRouter, Depends

from app.schemas.post import (
    PostCreate,
    PostUpdate,
)
from app.services.post_service import (
    list_posts,
    get_post,
    create_post,
    update_post,
    delete_post,
)
from app.services.auth_service import get_current_user

router = APIRouter()


@router.get("")
async def get_all_posts():
    return await list_posts()


@router.get("/{post_id}")
async def get_single_post(post_id: str):
    return await get_post(post_id)


@router.post("")
async def add_post(post: PostCreate, current_user: dict = Depends(get_current_user)):
    return await create_post(post)


@router.put("/{post_id}")
async def edit_post(
    post_id: str,
    post: PostUpdate,
    current_user: dict = Depends(get_current_user),
):
    return await update_post(post_id, post)


@router.delete("/{post_id}")
async def remove_post(post_id: str, current_user: dict = Depends(get_current_user)):
    return await delete_post(post_id)
