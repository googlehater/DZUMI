from fastapi import Depends
from dto.document_dto import DocumentDTO
from dao.documents_dao import DocumentDAO
from dao.documet_attributes_dao import DocumentAttributeDAO
from dao.users_dao import UserDAO
import dependencies

class DocumentService:
    def __init__(self, documents_dao: DocumentDAO, document_attribute_dao: DocumentAttributeDAO, user_dao: UserDAO):
        self.documents_dao = documents_dao
        self.document_attribute_dao = document_attribute_dao
        self.user_dao = user_dao
    
    async def load_new_document(self, document_dto: DocumentDTO):
        new_document = await self.documents_dao.create(document_dto)
        return new_document