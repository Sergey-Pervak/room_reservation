# app/models/meeting_room.py
from typing import List

# Импортируем из Sqlalchemy нужные классы и функции:
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Импортируем базовый класс для моделей и миксин:
from app.core.db import Base, CommonMixin


class MeetingRoom(CommonMixin, Base):
    # Имя переговорки должно быть не больше 100 символов,
    # уникальным и непустым.
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    # Новый атрибут модели.
    description: Mapped[str] = mapped_column(String, nullable=True)

    # Установите связь между моделями через функцию relationship.
    # Обратите внимание: название ссылающейся модели указано в кавычках!
    reservations: Mapped[List['Reservation']] = relationship(cascade='delete')
