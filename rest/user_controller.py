from fastapi import FastAPI, HTTPException, Depends, Query, APIRouter
from pydantic import BaseModel
from services.user_service import UserService
from dependencies import get_user_service
from typing import List, Optional
from dto.user_dto import UserDto, ChangeFirstNameDto, ChangePhoneNumberDto, ChangeRoleDto

# app = FastAPI()
router = APIRouter(prefix="/api/v1/users", tags=["users"])

# class UserDto(BaseModel):
#     last_name = [str]
#     first_name = [str]
#     middle_name = [str]
#     email = [str]
#     phone_number = [str]
#     role_id = [str]

# class ChangeFirstNameDto(BaseModel):
#     new_first_name = [str]

# class ChangePhoneNumberDto(BaseModel):
#     phone_number = [str]

# class ChangeRoleDto(BaseModel):
#     new_role = [str]

@router.get('/create_new/{user_dto.email}')
async def create_new_user(user_dto: UserDto,
                          user_service: UserService = Depends(get_user_service)
):
    user_service.create_user(user_dto)

@router.get('/change/first_name')
async def change_first_name(change_first_name_dto: ChangeFirstNameDto,
                          user_service: UserService = Depends(get_user_service)
):
    user_service.change_first_name(change_first_name_dto)

@router.get('/change/phone_number')
async def change_phone_number(change_phone_number_dto: ChangePhoneNumberDto,
                          user_service: UserService = Depends(get_user_service)):
    user_service.change_phone_number(change_phone_number_dto)

@router.get('/change/role')
async def change_role(change_role_dto: ChangeRoleDto,
                      user_service: UserService = Depends(get_user_service)):
    user_service.change_role(change_role_dto)