import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.base import Base



load_dotenv()

string_con = f"{os.getenv('DB_DRIVER')}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(string_con,
                       echo=True)
session = Session(engine)



bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class DBSession(Base):
    
    __tablename__ = "users"
    ###


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()
    