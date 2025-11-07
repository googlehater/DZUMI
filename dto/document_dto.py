from pydantic import BaseModel


class DocumentDTO(BaseModel):
    file_name: str