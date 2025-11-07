from pydantic import BaseModel
from typing import List, Optional


class UserDto(BaseModel):
    last_name: str
    first_name: str
    middle_name: str
    email: str
    phone_number: str
    role_id: str


class ChangeFirstNameDto(BaseModel):
    new_first_name: str


class ChangePhoneNumberDto(BaseModel):
    phone_number: str


class ChangeRoleDto(BaseModel):
    new_role: str
