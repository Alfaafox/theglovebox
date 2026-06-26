from pydantic import BaseModel, Field
from typing import Optional


class BrandCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: Optional[str] = None
    website: Optional[str] = None
    logo: Optional[str] = None


class BrandUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    country: Optional[str] = None
    website: Optional[str] = None
    logo: Optional[str] = None


class BrandResponse(BaseModel):
    id: int
    name: str
    country: Optional[str]
    website: Optional[str]
    logo: Optional[str]
    created_at: int
