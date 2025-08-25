from fastapi import FastAPI, HTTPException, Depends, Query, Path, APIRouter
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
# from services.orders_service import OrderService
from typing import List, Optional
from passlib.context import CryptContext
from datetime import timedelta, datetime
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

session_storage = {}

app = FastAPI()

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequestDto(BaseModel):
    username: str
    password: str 

class LoginRequestDto(BaseModel):
    username: str
    password: str

class TokenDto(BaseModel):
    access_token: str
    token_type: str 

class UserInDB(BaseModel):
    id: int
    username: str
    hashed_password: str
    created_at: datetime

class Session(BaseModel):
    session_id: int
    user_id: int
    created_at: datetime
    expires_at: datetime


def create_session(user_id: str) -> str:
    session_id = str(uuid.uuid4())
    session_storage[session_id] = {
        "user_id": user_id,
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=24)
    }
    return session_id

def get_session(session_id: str):
    '''Получает сессию по ID'''
    return session_storage.get(session_id)

def delete_session(session_id: str):
    '''Удаляет сессию'''
    if session_id in session_storage:
        del session_storage[session_id]


        ##

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

