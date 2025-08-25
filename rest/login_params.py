from fastapi import FastAPI, HTTPException, Depends, Query, Path
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
# from services.orders_service import OrderService
from typing import List, Optional
from passlib.context import CryptContext
from datetime import timedelta, datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


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

