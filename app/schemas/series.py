from pydantic import BaseModel, Field
from typing import Optional


class SeriesCreate(BaseModel):
    brand_id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class SeriesUpdate(BaseModel):
    brand_id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None


class SeriesResponse(BaseModel):
    id: int
    brand_id: int
    name: str
    description: Optional[str]
    created_at: int
