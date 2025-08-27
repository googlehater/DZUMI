from fastapi import APIRouter, HTTPException, Request, Response, Depends
from passlib.context import CryptContext
from database import get_db, DBSession as SessionModel
from models.user import User
from dao.users_dao import UserDAO
from pydantic import BaseModel
from sqlalchemy.orm import Session
from rest.login_params import LoginRequestDto
from dao.users_dao import UserDAO
from models.sessions import DBSession 
from datetime import datetime, timedelta
import uuid


router = APIRouter(prefix='/auth', tags=['auth'])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CreateUserRequestDto(BaseModel):
    username: str
    password: str 



def hash_password(password: str):
    '''Хеширует пароль используя HS256'''
    return bcrypt_context.hash(password)

def verify_password(plained_password: str, hashed_password: str) -> bool:
    '''Сравнивает чистый пароль с хешем'''
    return bcrypt_context.verify(plained_password, hashed_password)


@router.post('api/v1/register')
async def register(user_data: CreateUserRequestDto, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='User already exists')

    hashed_password = hash_password(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh()

    return {'message': 'User created successfuly', 'user_id': new_user.id}


@router.post('/api/v1/login')
async def login(login_data: LoginRequestDto, response: Response, db: Session = Depends(get_db)):
    '''Аутентифицирует пользователя и создает сессию'''

    user = UserDAO.get_user_by_username(login_data.username)
    if not user: 
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Проверяем пароль
    if verify_password(login_data.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    session_id = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(hours=24)

    new_session = DBSession(
        session_id = session_id,
        user_id = user.id,
        expires_at = expires_at
    )

    db.add(new_session)
    db.commit()

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=24*60*60, # сутки
        secure=False,
        samesite="lax"
    )

    return {"message": "Login successful", "user_id": user.id}


@router.post('/api/v1/logout')
async def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    '''Выход пользователя'''
    
    session_id = request.cookies.get("session_id")

    if session_id:
        # удаляем сессию
        session = db.query(DBSession).filter(DBSession.session_id == session_id).first()
        if session:
            db.delete(session)
            db.commit()

    # удаляем куки
    response.delete_cookie("session_id")

    return {"message": "Logout complete"}

