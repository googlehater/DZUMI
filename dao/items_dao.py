from sqlalchemy.orm import Session
from models.item import Item
from .base_dao import BaseDAO


class ItemDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session, Item)
