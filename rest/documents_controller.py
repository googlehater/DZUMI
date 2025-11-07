from fastapi import FastAPI, HTTPException, Depends, Query, APIRouter
from pydantic import BaseModel
from services.documents_service import DocumentService
from dependencies import get_document_service
from typing import List, Optional
from dto.document_dto import DocumentDTO

# app = FastAPI()
router = APIRouter(prefix='/api/v1/documents')

# class DocumentDTO(BaseModel):
#     file_name = [str]

@router.post('/load')
async def load_document(document_dto: DocumentDTO,
                        documents_service: DocumentService = Depends(get_document_service)
):
    documents_service.load_new_document(document_dto)