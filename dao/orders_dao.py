from sqlalchemy.orm import Session
from models.order import Order
from .base_dao import BaseDAO
from sqlalchemy import select, update
from typing import List, Optional


class OrderDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session, Order)

    def get_by_priority(self, priority):
        return self.session.query(Order).filter(Order.priority == priority).all() 
        # self.session.query(Order)
        # self.session - это сессия SQLAlchemy, подключение к БД
        # .query(Order) - создаёт новый запрос (Query object) для модели Order
        # .filter(Order.priority == priority)
        # Order.priority - ссылается на столбец priority в таблице orders
        # == priority - сравнение с переданным значением
        # .all() Выполняет собранный запрос в БД, Возвращает все строки результата как список объектов Order
        # Если нет результатов - вернёт пустой список
        # Это типо базовая конструкция стоит на заметку взять

    def get_by_date(self, date):
        pass

    async def get_all_orders(self, skip: int, limit: int):  
        '''Пагинация'''
        return await self.get_all(skip=skip, limit=limit)
  

    def save(self, request):
        self.session.add(request)
        self.session.commit()
        return request

    def update_status(self, order_id, new_status):
        '''Меняем статус через модель'''
        order

        if not Order.order_status.can_transition(new_status):
            raise ValueError("Невозможно перевести заявку в статус {new_status}")
        

        order = self.session.get(Order, order_id)
        order.change_status(new_status)
        self.save(order)

    def get_by_user(self, user: int) -> List[Order]:
        '''Получение заявок по пользователю'''
        query = select(Order).where(Order.user_id == user)
        result = self.session.execute(query)

        return result.scalars().all()
    
    def get_by_id(self, order_id: int) -> Optional[Order]:
        '''Получает заявку по ID'''
        query = select(Order).where(Order.id == order_id)
        result = self.session.execute(query)

        return result.scalars().first()
    
    async def get_all_orders(self, skip: int, limit: int):  
        '''Пагинация'''
        return await self.order_dao.get_all(skip=skip, limit=limit)
 