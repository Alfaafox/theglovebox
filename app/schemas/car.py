from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from datetime import date


class CarCreate(BaseModel):
    brand_id: int
    manufacturer_id: int
    series_id: int

    name: str = Field(..., min_length=1, max_length=200)
    variant: Optional[str] = None
    scale: Optional[str] = None
    year: Optional[int] = None
    country: Optional[str] = None

    status: str = "owned"

    purchase_price: Optional[Decimal] = None
    purchase_date: Optional[date] = None
    purchase_location: Optional[str] = None

    estimated_value: Optional[Decimal] = None

    story: Optional[str] = None
    notes: Optional[str] = None


class CarUpdate(CarCreate):
    pass


class CarResponse(BaseModel):
    id: int

    brand_id: int
    manufacturer_id: int
    series_id: int

    name: str
    variant: Optional[str]
    scale: Optional[str]
    year: Optional[int]
    country: Optional[str]

    status: str

    purchase_price: Optional[Decimal]
    purchase_date: Optional[date]
    purchase_location: Optional[str]

    estimated_value: Optional[Decimal]

    story: Optional[str]
    notes: Optional[str]

    created_at: int
    updated_at: int
