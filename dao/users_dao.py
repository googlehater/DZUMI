from sqlalchemy.orm import Session
from models.user import User
from .base_dao import BaseDAO
from sqlalchemy import select


class UserDAO(BaseDAO):
    def __init__(self, session):
        super().__init__(session, User)

    def get_user_by_username(self, session: Session, username: str):
        '''Получение пользователя по username'''

        return session.query(User).where(User.username == username).first()
        
        