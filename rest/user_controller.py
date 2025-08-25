from fastapi import FastAPI, HTTPException, Depends, Query
from pydantic import BaseModel
from services.user_service import UserService
from dependencies import get_user_service
from typing import List, Optional

app = FastAPI()

class UserDto(BaseModel):
    last_name = [str]
    first_name = [str]
    middle_name = [str]
    email = [str]
    phone_number = [str]
    role_id = [str]

class ChangeFirstNameDto(BaseModel):
    new_first_name = [str]

class ChangePhoneNumberDto(BaseModel):
    phone_number = [str]

class ChangeRoleDto(BaseModel):
    new_role = [str]

@app.get('/')
async def create_new_user(user_dto: UserDto,
                          user_service: UserService = Depends(get_user_service)
):
    user_service.create_user(user_dto)

@app.get('')
async def change_first_name(change_first_name_dto: ChangeFirstNameDto,
                          user_service: UserService = Depends(get_user_service)
):
    user_service.change_first_name(change_first_name_dto)

@app.get('')
async def change_phone_number(change_phone_number_dto: ChangePhoneNumberDto,
                          user_service: UserService = Depends(get_user_service)):
    user_service.change_phone_number(change_phone_number_dto)

@app.get('')
async def change_role(change_role_dto: ChangeRoleDto,
                      user_service: UserService = Depends(get_user_service)):
    user_service.change_role(change_role_dto)