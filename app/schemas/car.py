from typing import List, Optional

from pydantic import BaseModel, Field


class CarCreate(BaseModel):
    name: str = Field(..., min_length=1)
    brand: Optional[str] = ""
    status: Optional[str] = "owned"
    variant: Optional[str] = ""
    tags: List[str] = []
    photo: Optional[str] = ""
    story: Optional[str] = ""


class CarUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    brand: Optional[str] = ""
    status: Optional[str] = "owned"
    variant: Optional[str] = ""
    tags: List[str] = []
    photo: Optional[str] = ""
    story: Optional[str] = ""


class CarResponse(BaseModel):
    id: str
    name: str
    brand: Optional[str]
    status: Optional[str]
    variant: Optional[str]
    tags: List[str]
    photo: Optional[str]
    story: Optional[str]
    created_at: int
