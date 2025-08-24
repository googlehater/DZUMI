from sqlalchemy import String, ForeignKey, Text, Integer, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .role import Role
    from .order import Order


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    last_name: Mapped[str] = mapped_column(String(100))
    first_name: Mapped[str] = mapped_column(String(100))
    middle_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(20))
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    is_active: Mapped[bool] = mapped_column(Boolean)
    username: Mapped[str] = mapped_column(String, nullable=False)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # связи
    role: Mapped[list["Role"]] = relationship(back_populates="users")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")

    
    
    