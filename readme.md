### Основные команды

Cоздать и активировать виртуальное окружение:
```bash
py -3.12 -m venv venv
```

```bash
source venv/Scripts/activate
```

Обновить PIP:
```bash
python -m pip install --upgrade pip
```

Установите FastAPI:
```bash
pip install fastapi==0.115.5
```

Установите дополнительный пакет pydantic-settings.
Gозволит работать с конфигурацией приложения через переменные окружения:
```bash
pip install pydantic-settings==2.6.1
```

Установите в виртуальное окружение веб-сервер Uvicorn:
```bash
pip install "uvicorn[standard]==0.32.1"
```

Для асинхронного подключения к SQLite нужен драйвер aiosqlite:
```bash
pip install aiosqlite==0.20.0
```

Установите в виртуальное окружение бандл (комплект):
```bash
pip install "sqlalchemy[asyncio]==2.0.30"
```

Установите в виртуальное окружение библиотеку Alembic:
```bash
pip install alembic==1.13.1
```

Если в документации ```http://127.0.0.1:8000/docs``` не работает выпадающий список с ```Enum``` обнови библиотеки:
```bash
pip install --upgrade fastapi pydantic
```

Установите в виртуальное окружение проекта бандл — библиотеку FastAPI Users с дополнениями для работы с ORM SQLAlchemy:
```bash
pip install "fastapi-users[sqlalchemy]==13.0.0"
```

Записать все зависимости в файл requirements.txt:
```bash
pip freeze > requirements.txt
```

Для подключения Alembic к проекту — нужно «инициализировать» его:
```bash
alembic init --template async alembic
```

Просмотр доступных команд:
```bash
alembic --help
```

В Alembic есть команда history, которая позволяет увидеть в терминале все миграции в хронологическом порядке
(если хотим подробнее, то добавть -v к команде, для просмотра актуальной миграции добавить -i):
```bash
alembic history
```

Посмотреть последнюю применённую миграцию:
```bash
alembic current
```

Выполните команду для автоматического создания файла миграции:
```bash
alembic revision --autogenerate -m "First migration"
```

Выполнение всех неприменённых миграций запускается командой:
```bash
alembic upgrade head
```

Чтобы отменить все миграции, которые были в проекте, используется команда:
```bash
alembic downgrade base
```

Для старта приложения выполните команду для запуска сервера:
```bash
uvicorn app.main:app
```

Чтобы включить автоматический перезапуск сервера — остановите сервер и запустите его с флагом ```--reload```:
```bash
uvicorn app.main:app --reload
```

Список настроек сервера можно вывести в терминал:
```bash
uvicorn --help
```

Используйте асинхронную библиотеку Aiogoogle
```bash
pip install aiogoogle==5.13.0
```
