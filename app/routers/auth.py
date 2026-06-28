from fastapi import APIRouter, Depends

from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import register_user, login_user, get_current_user

router = APIRouter()


@router.post("/api/auth/register", response_model=UserResponse)
async def register(data: UserRegister):
    return await register_user(data.username, data.password)


@router.post("/api/auth/login", response_model=TokenResponse)
async def login(data: UserLogin):
    return await login_user(data.username, data.password)


@router.get("/api/auth/me", response_model=UserResponse)
async def me(current_user: dict = Depends(get_current_user)):
    return current_user
