from fastapi import Depends
from dto.item_dto import ItemDto
from dao.items_dao import ItemDAO
from dao.order_items_dao import OrderItemDAO
from dao.users_dao import UserDAO


class ItemService:
    def __init__(self, item_dao: ItemDAO, order_item_dao: OrderItemDAO, user_dao: UserDAO):
        self.item_dao = item_dao
        self.order_item_dao = order_item_dao
        self.user_dao = user_dao
    
    async def add_item(self, item_dto: ItemDto):
        new_item = await self.order_item_dao.create(item_dto)
        return new_item

    async def delete_item(self, item_dto: ItemDto):
        item_to_delete = self.order_item_dao.delete(item_dto)
        return item_to_delete
    
    async def change_items(self, item_dto: ItemDto):
        item_to_change = await self.order_item_dao.update(item_dto)
        return item_to_change