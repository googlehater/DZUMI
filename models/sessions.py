from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from typing import TYPE_CHECKING

from .base import Base


if TYPE_CHECKING:
    from .user import User


class DBSession(Base):
    
    __tablename__ = "sessions"
    
    session_id: Mapped[int] = mapped_column(Integer, Primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now(datetime.timezone.utc))
    expores_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    user: Mapped[list["User"]] = relationship(back_populates="sessions")