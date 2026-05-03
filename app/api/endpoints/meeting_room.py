# app/api/meeting_room.py
from typing import Annotated

# from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Depends
# Импортируем класс асинхронной сессии для аннотации параметра.
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем асинхронный генератор сессий.
from app.core.db import get_async_session
# from app.crud.meeting_room import (
#     create_meeting_room, delete_meeting_room,
#     get_meeting_room_by_id, get_room_id_by_name,
#     read_all_rooms_from_db, update_meeting_room
# )
# Добавьте импорт зависимости, определяющей, 
# что текущий пользователь - суперюзер.
from app.core.user import current_superuser
# Вместо импорта шести функций импортируйте объект meeting_room_crud.
from app.crud.meeting_room import meeting_room_crud
# Импортируем модель, чтобы указать её в аннотации.
# from app.models.meeting_room import MeetingRoom
from app.schemas.meeting_room import (
    MeetingRoomCreate, MeetingRoomDB, MeetingRoomUpdate
)
from app.api.validators import check_name_duplicate, check_meeting_room_exists
# Список импортов должен пополниться такими строкам:
from app.crud.reservation import reservation_crud
from app.schemas.reservation import ReservationDB


# # Для подключения эндпоинтов создадим роутер
# # и потом подключим его к объекту приложения.
# # Добавьте параметр prefix.
# router = APIRouter(
#     prefix='/meeting_rooms',
#     tags=['Meeting Rooms']
# )
# Объявляем роутер без параметров:
router = APIRouter() 

# Объявляем зависимость в отдельном объекте;
# этот объект будет доступен во всём модуле.
# Объект-зависимость для проброса сессии в обработчики:
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

@router.post(
    # '/meeting_rooms',
    # Оставьте только закрывающий слеш.
    # К этому пути будет дописываться префикс, в итоге получится адрес /meeting_rooms
    '/',
    # Указываем схему в параметре response_model:
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    # Добавьте вызов зависимости при обработке запроса.
    dependencies=[Depends(current_superuser)],
)
async def create_new_meeting_room(
        meeting_room: MeetingRoomCreate,
        # Указываем зависимость как параметр функции.
        # session: AsyncSession = Depends(get_async_session),
        # Указываем созданный объект Annotated как тип для параметра функции:
        session: SessionDep,
):
    # Добавляем докстринг для большей информативности.
    """Только для суперюзеров."""
    # # # Вызываем функцию проверки уникальности поля name:
    # # room_id = await get_room_id_by_name(meeting_room.name)

    # # Передаём сессию в CRUD-функцию:
    # room_id = await get_room_id_by_name(meeting_room.name, session)
    # # Если такой объект уже есть в базе - вызываем ошибку:
    # if room_id is not None:
    #     raise HTTPException(
    #         status_code=422,
    #         detail='Переговорка с таким именем уже существует!',
    #     )
    # # Вызываем crud-функцию, которая будет сохранять полученные данные в БД.
    # # Вызываем create_meeting_room(), 
    # # # эта функция возвращает объект ORM-модели MeetingRoom:
    # # new_room = await create_meeting_room(meeting_room)

    # # Передаём сессию в CRUD-функцию:
    # new_room = await create_meeting_room(meeting_room, session)
    # return new_room
    # # Функция возвращает объект ORM-модели, но в ответе клиент получит объект схемы!
    # # В работу включается магия FastAPI, и объект модели автоматически преобразуется 
    # # в объект Pydantic-схемы, указанной в параметре response_model.

    # Выносим проверку дубликата имени в отдельную корутину.
    # Если такое имя уже существует, то будет вызвано исключение HTTPException
    # и обработка запроса остановится.
    await check_name_duplicate(meeting_room.name, session)
    # new_room = await create_meeting_room(meeting_room, session)
    # Замените вызов функции на вызов метода.
    new_room = await meeting_room_crud.create(meeting_room, session)
    return new_room

@router.get(
    # '/meeting_rooms',
    # Оставьте только закрывающий слеш.
    # К этому пути будет дописываться префикс, в итоге получится адрес /meeting_rooms
    '/',
    response_model=list[MeetingRoomDB],
    response_model_exclude_none=True,
)
async def get_all_meeting_rooms(
        session: SessionDep,
):
    # Замените вызов функции на вызов метода.
    all_rooms = await meeting_room_crud.get_multi(session)
    # all_rooms = await read_all_rooms_from_db(session)
    # if all_meeting_rooms is None:
    #     raise HTTPException(
    #         status_code=422,
    #         detail='Данных нет!',
    #     )
    return all_rooms

@router.patch(
    # id обновляемого объекта будет передаваться path-параметром.
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    # Новая зависимость.
    dependencies=[Depends(current_superuser)],
)
async def partially_update_meeting_room(
        # id обновляемого объекта.
        meeting_room_id: int,
        # JSON-данные, отправленные пользователем.
        obj_in: MeetingRoomUpdate,
        session: SessionDep,
):
    # Добавляем докстринг для большей информативности.
    """Только для суперюзеров."""
    # # Вызываем get_meeting_room_by_id(): пытаемся получить по id объект из БД.
    # # В ответ ожидаем либо None, либо объект класса MeetingRoom.
    # meeting_room = await get_meeting_room_by_id(
    #     meeting_room_id, session
    # )
    # # Если объекта с запрошенным id нет в БД...
    # if meeting_room is None:
    #     raise HTTPException(
    #         # ...вернём статус 404 — Not found.
    #         status_code=404,
    #         detail='Переговорка не найдена!'
    #     )

    # Убрали проверку существования объекта
    # в отдельную корутину check_meeting_room_exists();
    # вызываем её:
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )

    if obj_in.name is not None:
        # Если в запросе получено поле name — проверяем его на уникальность.
        await check_name_duplicate(obj_in.name, session)

    # # Передаём в корутину все данные, необходимые для обновления объекта.
    # meeting_room = await update_meeting_room(
    #     meeting_room, obj_in, session
    # )
    # Замените вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.update(
        meeting_room, obj_in, session
    )
    return meeting_room

@router.delete(
    '/{meeting_room_id}',
    response_model=MeetingRoomDB,
    response_model_exclude_none=True,
    # Новая зависимость.
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
        meeting_room_id: int,
        session: SessionDep,
):
    # Добавляем докстринг для большей информативности.
    """Только для суперюзеров."""
    # Вызываем корутину, проверяющую существование запрошенного объекта.
    meeting_room = await check_meeting_room_exists(
        meeting_room_id, session
    )
    # meeting_room = await delete_meeting_room(
    #     meeting_room, session
    # )
    # Замените вызов функции на вызов метода.
    meeting_room = await meeting_room_crud.remove(meeting_room, session)
    return meeting_room

# # Корутина, проверяющая уникальность полученного имени переговорки.
# async def check_name_duplicate(
#         room_name: str,
#         session: AsyncSession,
# ) -> None:
#     # room_id = await get_room_id_by_name(room_name, session)
#     # Замените вызов функции на вызов метода.
#     room_id = await meeting_room_crud.get_room_id_by_name(room_name, session)
#     if room_id is not None:
#         raise HTTPException(
#             status_code=422,
#             detail='Переговорка с таким именем уже существует!',
#         )

# # Новая корутина: через функцию get_meeting_room_by_id() пытается
# # получить объект по ID и 
# # либо выбрасывает исключение,
# # либо возвращает полученный объект.
# async def check_meeting_room_exists(
#         meeting_room_id: int,
#         session: AsyncSession,
# ) -> MeetingRoom:
#     # meeting_room = await get_meeting_room_by_id(
#     #     meeting_room_id, session
#     # )
#     # Замените вызов функции на вызов метода.
#     meeting_room = await meeting_room_crud.get(meeting_room_id, session)
#     if meeting_room is None:
#         raise HTTPException(
#             status_code=404,
#             detail='Переговорка не найдена!'
#         )
#     return meeting_room

@router.get(
    '/{meeting_room_id}/reservations',
    response_model=list[ReservationDB],
    # Добавляем множество с полями, которые надо исключить из ответа.
    response_model_exclude={'user_id'},
)
async def get_reservations_for_room(
        meeting_room_id: int,
        session: SessionDep,
):
    await check_meeting_room_exists(meeting_room_id, session)
    reservations = await reservation_crud.get_future_reservations_for_room(
        room_id=meeting_room_id, session=session
    )
    return reservations
