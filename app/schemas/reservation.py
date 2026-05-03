# app/schemas/reservation.py
# Допишите новый импорт:
from typing import Optional
from datetime import datetime, timedelta

# Добавьте импорт Field из pydantic
from pydantic import (
    BaseModel, ConfigDict, Field, field_validator, model_validator
)
from typing_extensions import Self


# Представить объект datetime в виде строки с точностью до минут.
FROM_TIME = (
    datetime.now() + timedelta(minutes=10)
).isoformat(timespec='minutes')

TO_TIME = (
    datetime.now() + timedelta(hours=1)
).isoformat(timespec='minutes')


class ReservationBase(BaseModel):
    from_reserve: datetime = Field(..., examples=[FROM_TIME])
    to_reserve: datetime = Field(..., examples=[TO_TIME])

    model_config = ConfigDict(
        extra='forbid',
        json_schema_extra={
            'example': {
                'from_reserve': '2028-04-24T11:00',
                'to_reserve': '2028-04-24T12:00',
                'meetingroom_id': 1,
            }
        }
    )


# Схема для полученных данных (обновление объекта).
class ReservationUpdate(ReservationBase):
    
    @field_validator('from_reserve')
    @classmethod
    def check_from_reserve_later_than_now(cls, value):
        if value <= datetime.now():
            error = (
                'Время начала бронирования '
                'не может быть меньше текущего времени'
            )
            raise ValueError(error)
        return value

    @model_validator(mode='after')
    def check_from_reserve_before_to_reserve(self) -> Self:
        if self.from_reserve >= self.to_reserve:
            error = (
                'Время начала бронирования '
                'не может быть больше времени окончания'
            )
            raise ValueError(error)
        return self


# Схема для полученных данных (создание объекта).
# Этот класс наследуем от ReservationUpdate с валидаторами.
class ReservationCreate(ReservationUpdate):
    meetingroom_id: int


# Класс ReservationDB нельзя наследовать от ReservationCreate:
# тогда унаследуется и валидатор check_from_reserve_later_than_now(),
# и при получении старых объектов из БД он будет выдавать ошибку валидации:
# ведь их from_time вполне может быть меньше текущего времени.
# Схема для возвращаемого объекта.
class ReservationDB(ReservationBase):
    id: int
    meetingroom_id: int
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
