from fastapi import Depends
from sqlalchemy.orm import Session

from services.orders_service import OrderService
from services.documents_service import DocumentService
from services.user_service import UserService
from services.items_service import ItemService

from dao.orders_dao import OrderDAO
from dao.users_dao import UserDAO
from dao.documents_dao import DocumentDAO
from dao.documet_attributes_dao import DocumentAttributeDAO
from dao.items_dao import ItemDAO
from dao.order_items_dao import OrderItemDAO

from database import get_db

# тут мы пишем функции для Depends чтобы не явно/не строго передавать зависимости
# упрощает тесты

def get_order_dao(db: Session = Depends(get_db)):
    return OrderDAO(session=db)

def get_user_dao(db: Session = Depends(get_db)):
    return UserDAO(session = db)

def get_document_dao():
    return DocumentDAO

def get_document_attribute_dao():
    return DocumentAttributeDAO

def get_item_dao():
    return ItemDAO

def get_order_item_dao():
    return OrderItemDAO

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_order_service(
    order_dao: OrderDAO = Depends(get_order_dao),
    user_dao: UserDAO = Depends(get_user_dao)
):
    return OrderService(order_dao, user_dao)

def get_document_service(
        document_dao: DocumentDAO = Depends(get_document_dao),
        document_attribute_dao: DocumentAttributeDAO = Depends(get_document_attribute_dao),
        user_dao: UserDAO = Depends(get_user_dao)
):
    return DocumentService(document_dao, document_attribute_dao, user_dao)

def get_user_service(
        user_dao: UserDAO = Depends(get_user_dao)
):
    return UserService(user_dao)

def get_item_service(
        item_dao: ItemDAO = Depends(get_item_dao),
        order_item_dao: OrderItemDAO = Depends(get_order_item_dao),
        user_dao: UserDAO = Depends(get_user_dao)
):
    return ItemService
