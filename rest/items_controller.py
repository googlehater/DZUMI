from fastapi import FastAPI, HTTPException, Depends, Query, Path, APIRouter
from dto.item_dto import ItemDto
from services.items_service import ItemService
from dependencies import get_item_service
from typing import List, Optional

# app = FastAPI()
router = APIRouter(prefix='/api/v1/items', tags=["items"])

# Вот это что? это неверная дтошка вроде - убить
# class ItemDto(BaseModel):
#     item_id = [int]
#     order_id = [int]
#     quantity = [int]


# Вот так надо
# class ItemDto(BaseModel):
#     item_id: int
#     order_id: int
#     quantity: int
#     supplier_id: int
    # как будет выбираться supplier_id? типо выбираться из списка
    # или что то такое, а потом браться id. я так думаю, нет?
    # - андрей


# я думаю как будет, у нас есть в бд таблица с товаром и типо таблица с корзинами
# добавляем товар -> у него свой айди и в таблице с корзинами у него будет айди заказа к которому он относится
# если не понял посмотри еще раз бд/модели

# понял, делаем
# - андрей


@router.post('/add_item/{order_id}')
async def add_item(
    item_dto: ItemDto,
    item_service: ItemService = Depends(get_item_service),
    order_id: int = Path(..., title='ID заявки'),
):
    new_item = await item_service.add_item(item_dto)
    return new_item

