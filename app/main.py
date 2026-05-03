# Импортируем декоратор для функции lifespan():
from contextlib import asynccontextmanager

from fastapi import FastAPI

# Импортируем роутер.
# from app.api.endpoints.meeting_room import router
# Импортируем главный роутер.
from app.api.routers import main_router
# Импортируем настройки проекта из config.py.
from app.core.config import settings
# Импортируем корутину для создания первого суперюзера:
from app.core.init_db import create_first_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Всё, что указано выше yield, выполняется до запуска приложения.
    await create_first_superuser()

    # Lifespan-функция обязана вызывать yield,
    # но не должна возвращать никаких значений.
    yield

    # Все инструкции, описанные после yield,
    # выполняется перед завершением работы приложения.
    # В нашем случае ничего выполнять не нужно, но можно и пошалить:
    # print('И все эти мгновения исчезнут во времени, как слёзы под дождём.')

# Устанавливаем заголовок приложения при помощи аргумента title,
# в качестве значения указываем атрибут app_title объекта settings.
# Объект функции lifespan передаётся в аргумент lifespan объекта приложения.
app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan
)

# # Подключаем роутер.
# app.include_router(router)

# Подключаем главный роутер к объекту приложения:
app.include_router(main_router)
