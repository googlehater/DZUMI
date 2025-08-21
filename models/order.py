from sqlalchemy import String, ForeignKey, Text, Integer, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum, unique 
from typing import TYPE_CHECKING
from sqlalchemy import Enum as SQLEnum


from .base import Base

if TYPE_CHECKING:
    from .object import Object
    from .user import User
    from .document import Document
    from .order_items import OrderItem


@unique
class OrderStatusEnum(Enum):

    NEW = "NEW"
    UNDER_APPROVAL = "UNDER_APPROVAL"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELED = "CANCELED"

    # Куда может перейти состояние
    transitions = {
        NEW: [UNDER_APPROVAL, CANCELED],
        UNDER_APPROVAL: [IN_PROGRESS, CANCELED],
        IN_PROGRESS: [DONE, CANCELED],
        DONE: [],
        CANCELED: [] 
    }
    
    def can_transition(self, new_status):
        return new_status in self.transitions[self]

    @classmethod
    def describe_dictionary(self):
        yield self.NEW, "Новая"
        yield self.UNDER_APPROVAL, "На согласовании"
        yield self.IN_PROGRESS, "В работе"
        yield self.DONE, "Выполнено"
        yield self.CANCELED, "Отменено"


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    object_id: Mapped[int] = mapped_column(ForeignKey('objects.id', ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    system_type_id: Mapped[str] = mapped_column(String(70))  # enum
    order_status: Mapped[OrderStatusEnum] = mapped_column(
        SQLEnum(OrderStatusEnum),
        default=OrderStatusEnum.NEW,
        nullable=False
    )
    total_price: Mapped[float] = mapped_column(Numeric(10, 2))
    agreed: Mapped[str] = mapped_column(String(50))
    priority: Mapped[str] = mapped_column(String(50))  # enum
    description: Mapped[str] = mapped_column(Text)
    comment: Mapped[str] = mapped_column(Text)
    decline_reason: Mapped[str] = mapped_column(String(255))

    # связи
    document: Mapped[list["Document"]] = relationship(back_populates="order")
    object: Mapped["Object"] = relationship(back_populates="orders")
    user: Mapped["User"] = relationship(back_populates="orders")
    order_item: Mapped[list["OrderItem"]] = relationship(back_populates="order")
    

    def change_status(self, new_status: OrderStatusEnum):
        '''Проверяет и изменяет статус заявки'''
        if self.order_status.can_transition(new_status):
            self.order_status = new_status
        else:
            raise ValueError(f"Нельзя перейти из {self.order_status} в {new_status}")

    def status_display_name(self) -> str:
        '''Возвращает название статуса'''
        return OrderStatusEnum.describe_dictionary(self.order_status)
    
