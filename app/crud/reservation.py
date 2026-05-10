# app/crud/reservation.py
# Новый импорт.
from typing import Optional
# Новый импорт для аннотации параметров.
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, between, func, or_, select

from app.crud.base import CRUDBase
# Импортируем модель пользователя:
from app.models import Reservation, User


# reservation_crud = CRUDBase(Reservation)


# Новый класс должен быть унаследован от CRUDBase.
class CRUDReservation(CRUDBase):
    # async def get_reservations_at_the_same_time(
    #         self,
    #         from_reserve: datetime,
    #         to_reserve: datetime,
    #         meetingroom_id: int,
    #         session: AsyncSession,
    # ) -> list[Reservation]:
    #     reservations = await session.execute(
    #         select(Reservation).where(
    #             Reservation.meetingroom_id == meetingroom_id,
    #             or_(
    #                 between(
    #                     from_reserve,
    #                     Reservation.from_reserve,
    #                     Reservation.to_reserve
    #                 ),
    #                 between(
    #                     to_reserve,
    #                     Reservation.from_reserve,
    #                     Reservation.to_reserve
    #                 ),
    #                 and_(
    #                     from_reserve <= Reservation.from_reserve,
    #                     to_reserve >= Reservation.to_reserve
    #                 )
    #             )
    #         )
    #     )
    #     reservations = reservations.scalars().all()
    #     return reservations
# Выбрать такие объекты Reservation, где выполняются следующие условия:
#     номер переговорки равен заданному 
#     и
#     верно одно из следующих условий:
#         начало новой брони лежит между началом и концом брони существующего объекта,
#         или
#         конец новой брони лежит между началом и концом брони существующего объекта,
#         или
#         (начало новой брони меньше начала брони существующего объекта
#          и
#          конец новой брони больше конца брони существующего объекта)

    # # Более короткий вариант решения:
    # async def get_reservations_at_the_same_time(
    #         self,
    #         from_reserve: datetime,
    #         to_reserve: datetime,
    #         meetingroom_id: int,
    #         session: AsyncSession,
    # ) -> list[Reservation]:
    #     reservations = await session.execute(
    #         select(Reservation).where(
    #             Reservation.meetingroom_id == meetingroom_id,
    #             and_(
    #                 from_reserve <= Reservation.to_reserve,
    #                 to_reserve >= Reservation.from_reserve
    #             )
    #         )
    #     )
    #     reservations = reservations.scalars().all()
    #     return reservations

# Выбрать такие объекты Reservation, где выполняются следующие условия:
#     номер переговорки равен заданному 
#     и
#     одновременно верны следующие условия:
#         начало новой брони меньше или равно окончанию брони существующего объекта,
#         окончание новой брони больше или равно началу брони существующего объекта. 

    async def get_reservations_at_the_same_time(
        self,
        # Добавляем звёздочку, чтобы обозначить, что все дальнейшие параметры
        # должны передаваться по ключу. Это позволит располагать
        # параметры со значением по умолчанию перед параметрами без таких значений.
        # Это позволит логично скомпоновать параметры:
        # сначала данные, потом всё остальное.
        *,
        from_reserve: datetime,
        to_reserve: datetime,
        meetingroom_id: int,
        # Добавляем новый опциональный параметр - id объекта бронирования.
        reservation_id: int | None = None,
        session: AsyncSession,
    ) -> list[Reservation]:
        # Выносим существующий запрос к БД в отдельное выражение.
        statement = select(Reservation).where(
            Reservation.meetingroom_id == meetingroom_id,
            and_(
                from_reserve <= Reservation.to_reserve,
                to_reserve >= Reservation.from_reserve
            )
        )
        # Если передан id бронирования...
        if reservation_id is not None:
            # ... то к выражению нужно добавить новое условие.
            statement = statement.where(
                # id искомых объектов не должны быть равны id обновляемого объекта.
                Reservation.id != reservation_id
            )
        # Выполняем запрос.
        reservations = await session.execute(statement)
        reservations = reservations.scalars().all()
        return reservations

    async def get_future_reservations_for_room(
            self,
            room_id: int,
            session: AsyncSession,
    ):
        reservations = await session.execute(
            # Получить все объекты Reservation...
            select(Reservation).where(
                # ...где внешний ключ meetingroom_id
                # равен id запрашиваемой переговорки...
                Reservation.meetingroom_id == room_id,
                # ...а время конца бронирования больше текущего времени.
                Reservation.to_reserve > datetime.now()
            )
        )
        reservations = reservations.scalars().all()
        return reservations

    # Новый метод:
    async def get_by_user(
            self, session: AsyncSession, user: User
    ):
        reservations = await session.execute(
            select(Reservation).where(
                Reservation.user_id == user.id
            )
        )
        return reservations.scalars().all()

    # Новый метод
    async def get_count_res_at_the_same_time(
            self,
            from_reserve: datetime,
            to_reserve: datetime,
            session: AsyncSession,
    ) -> list[dict[str, int]]:
        reservations = await session.execute(
            # Получаем количество бронирований переговорок за период
            select(Reservation.meetingroom_id,
                    func.count(Reservation.meetingroom_id)).where(
                Reservation.from_reserve >= from_reserve,
                Reservation.to_reserve <= to_reserve
            ).group_by(Reservation.meetingroom_id)
        )
        reservations = reservations.all()
        res = [
            {"meetingroom_id": room_id, "count": count}
            for room_id, count in reservations
        ]
        return res

# Создаём объекта класса CRUDReservation.
reservation_crud = CRUDReservation(Reservation)
