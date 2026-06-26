from pydantic import BaseModel


class ImageResponse(BaseModel):
    id: str
    car_id: str
    filename: str
    original_name: str
    image_type: str
    display_order: int
    created_at: int
