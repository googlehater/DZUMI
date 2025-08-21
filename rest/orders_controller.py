from fastapi import FastAPI, HTTPException, Depends, Query, Path
from pydantic import BaseModel
from services.orders_service import OrderService
from dependencies import get_order_service
from typing import List, Optional

app = FastAPI()

# дто может быть ДОХУЯ

class OrderCreateDto(BaseModel): # описывает какие данные ожидаются в теле запроса
    user_id: int
    object_id: int
    system_type_id: int
    description: str
    comment: Optional[str] = None
    decline_reason: Optional[str] = None


class OrderResponceDto(BaseModel):  # дто для ответа
    id: int
    object_id: int
    user_id: int  # мб поменять на ФИО
    system_type: int
    order_status: str
    total_price: float
    agreed: str
    priority: int
    description: str
    comment: str
    decline_reason: str

class OrderChangeStatusDto(BaseModel):
    user_id: int
    order_id: int
    new_order_status: str


@app.post('/api/v1/orders/order') # декоратор, обработчик пост запросов, в скобках потом эндпоинт юрлку вставим 
async def create_order(
    orders_dto: OrderCreateDto,
    orders_service: OrderService = Depends(get_order_service)
):
    orders_service.create_new_order(orders_dto) # заявка создана

# Эндпоинт с пагинацией
@app.get("/api/v1/orders", response_model=List[OrderResponceDto])
async def get_orders(
    skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: int = Query(10, le=100, description="Лимит записей на страницу"),
    order_service: OrderService = Depends(get_order_service)
):
    '''Получить все заявки (пагинация)'''
    return await order_service.get_all_orders(skip=skip, limit=limit)

# Смена статуса заявки
@app.patch('/api/v1/orders/order/{order_id}/change/status')
async def change_status_order(
    new_order_status: str,
    order_service: OrderService,
    order_status_dto: OrderChangeStatusDto,
    order_id: int = Path(..., title='ID заявки'),
    
): 
    '''Поменять статус на новый'''
    return await order_service.transit_order_status(order_status_dto, new_status=new_order_status)

