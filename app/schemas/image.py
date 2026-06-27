from typing import Optional
from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: int
    car_id: int
    filename: str
    thumbnail_filename: Optional[str] = None
    original_name: Optional[str] = None
    image_type: Optional[str] = None
    display_order: int
    is_primary: bool
    created_at: int
