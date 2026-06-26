from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


class PostUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)


class PostResponse(BaseModel):
    id: str
    title: str
    body: str
    created_at: int
