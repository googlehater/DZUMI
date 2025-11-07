from pydantic import BaseModel


class ItemDto(BaseModel):
    item_id: int
    order_id: int
    quantity: int
    supplier_id: int