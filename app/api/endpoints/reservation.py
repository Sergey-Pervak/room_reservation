# app/api/endpoints/reservation.py
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_meeting_room_exists,
    check_reservation_before_edit,
    check_reservation_intersections,
)
from app.core.db import get_async_session
# В список импортов должен быть добавлен суперюзер.
from app.core.user import current_superuser, current_user
from app.crud.reservation import reservation_crud
# Дополните импорт схем классом ReservationUpdate.
from app.schemas.reservation import (
    ReservationCreate, ReservationDB, ReservationUpdate
)
# Допишите новые импорты:
from app.core.user import current_user
from app.models import User


router = APIRouter()
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

@router.post('/', response_model=ReservationDB)
async def create_reservation(
        reservation: ReservationCreate,
        session: SessionDep,
        # Получаем текущего пользователя и сохраняем в переменную user.
        user: Annotated[User, Depends(current_user)]
):
    await check_meeting_room_exists(
        reservation.meetingroom_id, session
    )
    await check_reservation_intersections(
        # Так как валидатор принимает **kwargs, 
        # аргументы должны быть переданы с указанием ключей.
        **reservation.model_dump(), session=session
    )
    new_reservation = await reservation_crud.create(
        # Передаём объект пользователя в метод создания объекта бронирования.
        reservation, session, user
    )
    return new_reservation

@router.get(
    '/',
    response_model=list[ReservationDB],
    # Новая зависимость для эндпоинта.
    dependencies=[Depends(current_superuser)],
)
async def get_all_reservations(
    session: Annotated[AsyncSession, Depends(get_async_session)]
):
    # Добавляем докстринг для большей информативности.
    """Только для суперюзеров."""
    # reservations = await reservation_crud.get_multi(session)
    return await reservation_crud.get_multi(session)

@router.delete('/{reservation_id}', response_model=ReservationDB)
async def delete_reservation(
    reservation_id: int,
    session: SessionDep,
    # Новая зависимость.
    user: Annotated[User, Depends(current_user)],
):
    """Для суперюзеров или создателей объекта бронирования."""
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    reservation = await reservation_crud.remove(
        reservation, session
    )
    return reservation

@router.patch('/{reservation_id}', response_model=ReservationDB)
async def update_reservation(
    reservation_id: int,
    obj_in: ReservationUpdate,
    session: SessionDep,
    # Новая зависимость.
    user: Annotated[User, Depends(current_user)],
):
    """Для суперюзеров или создателей объекта бронирования."""
    # Проверяем, что запрошенный объект бронирования существует.
    reservation = await check_reservation_before_edit(
        reservation_id, session, user
    )
    # Проверяем, что нет пересечений с другими бронированиями.
    await check_reservation_intersections(
        # Новое время бронирования, распакованное на ключевые аргументы.
        **obj_in.model_dump(),
        # id обновляемого объекта бронирования:
        reservation_id=reservation_id,
        # id переговорки:
        meetingroom_id=reservation.meetingroom_id,
        session=session
    )
    reservation = await reservation_crud.update(
        db_obj=reservation,
        # На обновление передаём объект класса ReservationUpdate.
        obj_in=obj_in,
        session=session,
    )
    return reservation


# Новый эндпоинт.
@router.get(
    '/my_reservations',
    response_model=list[ReservationDB],
    # Добавляем множество с полями, которые надо исключить из ответа.
    response_model_exclude={'user_id'},
)
async def get_my_reservations(
        session: SessionDep,
        # Передаём зависимость в аргументы функции, а не декоратора.
        # В этой зависимости получаем обычного пользователя, а не суперюзера.
        user: Annotated[User, Depends(current_user)]
):
    # Сразу можно добавить докстринг для большей информативности.
    """Получает список всех бронирований для текущего пользователя."""
    # Вызываем созданный метод.
    reservations = await reservation_crud.get_by_user(
        session=session, user=user
    )
    return reservations
