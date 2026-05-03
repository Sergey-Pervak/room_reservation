# # app/crud/meeting_room.py
# from typing import Optional

# # Добавляем импорт функции select.
# from sqlalchemy import select
# # Импортируем класс асинхронной сессии для аннотаций.
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi.encoders import jsonable_encoder

# # # Импортируем AsyncSessionLocal из файла с настройками БД.
# # from app.core.db import AsyncSessionLocal
# from app.models.meeting_room import MeetingRoom
# from app.schemas.meeting_room import MeetingRoomCreate, MeetingRoomUpdate

# # Функция работает с асинхронной сессией, 
# # поэтому ставим ключевое слово async.
# # В функцию передаём схему MeetingRoomCreate.
# async def create_meeting_room(
#         new_room: MeetingRoomCreate,
#         # Добавляем новый параметр.
#         session: AsyncSession
# ) -> MeetingRoom:
#     # Конвертируем объект MeetingRoomCreate в словарь.
#     new_room_data = new_room.model_dump()

#     # Создаём объект модели MeetingRoom.
#     # Передаём в класс пары "ключ=значение", для этого распаковываем словарь.
#     db_room = MeetingRoom(**new_room_data)

#     # Убираем контекстный менеджер.
#     # # Создаём асинхронную сессию через контекстный менеджер.
#     # async with AsyncSessionLocal() as session:
#     #     # Добавляем созданный объект в сессию. 
#     #     # Никакие действия с базой пока ещё не выполняются.
#     #     session.add(db_room)

#     #     # Записываем изменения непосредственно в БД. 
#     #     # Так как сессия асинхронная, используем ключевое слово await.
#     #     await session.commit()
#     #     await session.refresh(db_room)

#     # Возвращаем только что созданный объект класса MeetingRoom.
#     session.add(db_room)
#     await session.commit()
#     return db_room

# # Добавляем новую асинхронную функцию.
# async def get_room_id_by_name(
#         room_name: str,
#         # Добавляем новый параметр.
#         session: AsyncSession
# ) -> Optional[int]:
#     # Убираем контекстный менеджер.
#     # async with AsyncSessionLocal() as session:
#     #     # Получаем объект класса Result.
#     #     db_room_id = await session.execute(
#     #         select(MeetingRoom.id).where(
#     #             MeetingRoom.name == room_name
#     #         )
#     #     )
#     db_room_id = await session.execute(
#         select(MeetingRoom.id).where(
#             MeetingRoom.name == room_name
#         )
#     )
#     # Извлекаем из Result конкретное значение.
#     db_room_id = db_room_id.scalars().first()
#     return db_room_id

# async def read_all_rooms_from_db(
#         session: AsyncSession
# ) -> list[MeetingRoom]:
#     db_rooms = await session.execute(select(MeetingRoom))
#     return list(db_rooms.scalars().all())

# async def get_meeting_room_by_id(
#         room_id: int,
#         session: AsyncSession
# ) -> Optional[MeetingRoom]:
#     db_room = await session.execute(
#         select(MeetingRoom).where(
#             MeetingRoom.id == room_id
#         )
#     )
#     db_room = db_room.scalars().first()
#     # Метод session.get — получаем объект модели MeetingRoom с указанным primary key:
#     # db_room = await session.get(MeetingRoom, room_id)
#     return db_room

# async def update_meeting_room(
#         # Объект из БД для обновления:
#         db_room: MeetingRoom,
#         # Объект из запроса:
#         room_in: MeetingRoomUpdate,
#         # Сессия:
#         session: AsyncSession,
# ) -> MeetingRoom:
#     # Конвертируем объект из БД в словарь:
#     obj_data = jsonable_encoder(db_room)
#     # Конвертируем объект с данными из запроса в словарь. 
#     # Добавляем параметр exclude_unset.
#     update_data = room_in.model_dump(exclude_unset=True)

#     # Сравниваем словари:
#     # перебираем все ключи словаря, сформированного из БД-объекта.
#     for field in obj_data:
#         # Если конкретное поле есть в словаре с данными из запроса, то...
#         if field in update_data:
#             # ...устанавливаем объекту из БД новое значение атрибута.
#             setattr(db_room, field, update_data[field])
#     # Добавляем обновлённый объект в сессию.
#     session.add(db_room)
#     # Фиксируем изменения.
#     await session.commit()
#     return db_room

# async def delete_meeting_room(
#         db_room: MeetingRoom,
#         session: AsyncSession,
# ) -> MeetingRoom:
#     # Передаём объект модели в метод session.delete().
#     await session.delete(db_room)
#     # Коммитим изменения.
#     await session.commit()
#     return db_room


# app/crud/meeting_room.py
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.meeting_room import MeetingRoom

# Создаем новый класс, унаследованный от CRUDBase.
class CRUDMeetingRoom(CRUDBase):

    # Вместо функции опишем метод класса.
    async def get_room_id_by_name(
        # Дописываем параметр self. 
        # В качестве альтернативы здесь можно 
        # применить декоратор @staticmethod.
        self,
        room_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_room_id = await session.execute(
            select(MeetingRoom.id).where(
                MeetingRoom.name == room_name
            )
        )
        db_room_id = db_room_id.scalars().first()
        return db_room_id

# Объект meeting_room_crud наследуем не от CRUDBase, 
# а от только что созданного класса CRUDMeetingRoom. 
# В инициализатор класса передаем модель, как и в CRUDBase.
meeting_room_crud = CRUDMeetingRoom(MeetingRoom)
