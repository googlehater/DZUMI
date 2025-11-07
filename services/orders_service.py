from fastapi import Depends, HTTPException
from dto.order_dto import OrderCreateDto, OrderChangeStatusDto
from dao.orders_dao import OrderDAO
from dao.users_dao import UserDAO
# import dependencies
from models.order import OrderStatusEnum  #, Order

class OrderService:
    def __init__(self, order_dao: OrderDAO, user_dao: UserDAO):
        self.order_dao = order_dao
        self.user_dao = user_dao
    
    def create_new_order(self, order_dto: OrderCreateDto):
        '''Создает заявку с проверкой пользователя'''
        user = self.user_dao.get_by_id(order_dto.user_id)
        if not user:
            raise ValueError("Пользователь не найден")
        
        order_data = order_dto.model_dump()
        new_order = self.order_dao.create(**order_data)

        return new_order
  
    async def transit_order_status(self, order_dto: OrderChangeStatusDto, new_status: str):
        '''Переводит заявку в новый статус'''
        try:
            status_enum = OrderStatusEnum(new_status)
        except: 
            raise ValueError(f"Неизвестный статус: {new_status}")
        
        user = await self.user_dao.get_by_id(order_dto.user_id)
        if not user: 
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        order = await self.order_dao.get_by_id(order_dto.order_id)
        if not order:
            raise ValueError("Заяка не найдена")
        
        
        current_status_enum = OrderStatusEnum(order.order_status)
        
        if not current_status_enum.can_transition(status_enum):
            raise ValueError(f"Невозможно перевести заявку в статус {new_status}")
        
        
        await self.order_dao.update_status(order.id, status_enum)
        return None

    async def get_all_orders(self, skip: int, limit: int):
        '''Пагинация'''
        order_list = self.order_dao.get_all_orders(skip=skip, limit=limit)
        return order_list
