from fastapi import FastAPI, HTTPException, Depends, Query, Path, APIRouter
from pydantic import BaseModel
from services.orders_service import OrderService
from dependencies import get_order_service
from typing import List, Optional
from dto.order_dto import OrderCreateDto, OrderResponceDto, OrderChangeStatusDto

# app = FastAPI()
router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

# дто может быть ДОХУЯ 
# поэтому я их вынес в отдельную директорию

# описывает какие данные ожидаются в теле запроса
# class OrderCreateDto(BaseModel): 
#     user_id: int
#     object_id: int
#     system_type_id: int
#     description: str
#     comment: Optional[str] = None
#     decline_reason: Optional[str] = None


# дто для ответа
# class OrderResponceDto(BaseModel):
#     id: int
#     object_id: int
#     user_id: int  # мб поменять на ФИО
#     system_type: int
#     order_status: str
#     total_price: float
#     agreed: str
#     priority: int
#     description: str
#     comment: str
#     decline_reason: str

# дто для изменения статуса заявки
# class OrderChangeStatusDto(BaseModel):
#     user_id: int
#     order_id: int
#     new_order_status: str


# Создать заявку
@router.post('/order', response_model=None) 
async def create_order(
    orders_dto: OrderCreateDto,
    orders_service: OrderService = Depends(get_order_service)
):
    orders_service.create_new_order(orders_dto) # заявка создана
    return {"status": "created"}

# Эндпоинт с пагинацией
@router.get("/order_list", response_model=List[OrderResponceDto])  #List[OrderResponceDto]
async def get_orders(
    skip: int = Query(0, ge=0, description="Сколько записей пропустить"),
    limit: int = Query(10, le=100, description="Лимит записей на страницу"),
    order_service: OrderService = Depends(get_order_service)
):
    '''Получить все заявки (пагинация)'''
    await order_service.get_all_orders(skip=skip, limit=limit)
    return {"status": "got-all-orders"}

# Смена статуса заявки
@router.put('/order/{order_id}/change/status', response_model=None)
async def change_status_order(
    new_order_status: str,
    order_status_dto: OrderChangeStatusDto,
    order_id: int = Path(..., title='ID заявки'), 
    order_service: OrderService = Depends(get_order_service)  
): 
    '''Поменять статус на новый'''
    
    await order_service.transit_order_status(order_dto=order_status_dto, new_status=new_order_status)
    return None

# Редактировать заявку
@router.patch('/order/{order_id}/change')
async def edit_order(
        order_id: int = Path(..., title='ID заявки'),
):
    pass

# похоже нахуй убирать это говно
# Работы для новой 
@router.post('/items/{order_id}')
async def add_items(

):
    pass


