# app/schemas/meeting_room.py

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


# Базовый класс схемы, от которого наследуем все остальные.
class MeetingRoomBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class MeetingRoomCreate(MeetingRoomBase):
    # Переопределяем атрибут name, делаем его обязательным.
    name: str = Field(..., min_length=1, max_length=100)
    # Описывать поле description не нужно: оно уже есть в базовом классе.


# Схема для обновления объектов: наследуемся от базовой схемы, но не изменяем её.
class MeetingRoomUpdate(MeetingRoomBase):
    @field_validator('name')
    @classmethod
    def name_cannot_be_null(cls, value):
        if value is None:
            error = 'Имя переговорки не может быть пустым!'
            raise ValueError(error)
        return value


# Возвращаемую схему унаследуем от MeetingRoomCreate, 
# чтобы снова не описывать обязательное поле name.
class MeetingRoomDB(MeetingRoomCreate):
    id: int

    # Добавьте в код атрибут from_attributes:
    model_config = ConfigDict(from_attributes=True)
