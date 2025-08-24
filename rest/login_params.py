from fastapi import FastAPI, HTTPException, Depends, Query, Path
from pydantic import BaseModel
from services.orders_service import OrderService
from typing import List, Optional
from passlib.context import CryptContext
from datetime import timedelta, datetime

app = FastAPI()

pwd_context = CryptContext(shemes=["bcrypt"], deprecated="auto")
SECRET_KEY = ""
ALGORYTHM = ""
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginRequestDto(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    '''Сравнивает открытый пароль с хешем'''
    pass

def authenticate_user(usr_name, password):
    '''Проверяет, существует ли пользователь'''
    pass

def create_access_token(data: dict, expires_delta: timedelta):
    
    pass

# Авторизация
@app.post('/api/v1/login')
async def login(login_req: LoginRequestDto):
    user = authenticate_user(login_req.username, login_req.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    return {"access_token": access_token, "token_type": "bearer"}





