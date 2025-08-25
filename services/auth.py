from fastapi import APIRouter, HTTPException, Request, Response, Depends
from passlib.context import CryptContext
from database import get_db, DBSession as SessionModel
from models.user import User
from dao.users_dao import UserDAO
from pydantic import BaseModel
from sqlalchemy.orm import Session


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


# @router.post('api/v1/login')
# async def login()
