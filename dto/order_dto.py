from pydantic import BaseModel
from typing import Optional


class OrderCreateDto(BaseModel): 
    user_id: int
    object_id: int
    system_type_id: int
    description: str
    comment: Optional[str] = None
    decline_reason: Optional[str] = None


class OrderResponceDto(BaseModel):
    id: int
    object_id: int
    user_id: int  # мб поменять на ФИО
    system_type_id: int
    order_status: str
    total_price: float
    agreed: str
    priority: Optional[str] = None
    description: Optional[str] = None
    comment: Optional[str] = None
    decline_reason: Optional[str] = None

    class Config:
        orm_model: True
        # Без orm_mode=True FastAPI 
        # не сможет сериализовать ORM объекты 
        # в JSON через Pydantic, что вызовет ошибки.


class OrderChangeStatusDto(BaseModel):
    user_id: int
    order_id: int
    new_order_status: str


