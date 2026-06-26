from fastapi import APIRouter

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

router = APIRouter()


@router.get("")
async def get_all_posts():
    return await list_posts()


@router.get("/{post_id}")
async def get_single_post(post_id: str):
    return await get_post(post_id)


@router.post("")
async def add_post(post: PostCreate):
    return await create_post(post)


@router.put("/{post_id}")
async def edit_post(
    post_id: str,
    post: PostUpdate,
):
    return await update_post(post_id, post)


@router.delete("/{post_id}")
async def remove_post(post_id: str):
    return await delete_post(post_id)

