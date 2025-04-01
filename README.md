# To-Do App API

To-Do App API — это RESTful веб-сервис, который позволяет пользователям управлять задачами (tasks), категориями (categories) и профилями пользователей (users). Проект использует FastAPI, SQLAlchemy и JWT для аутентификации.

## Установка и запуск
1. Клонирование репозитория
```bash
git clone https://github.com/your-repo/todo-app-api.git
cd todo-app-api

```
2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. Установка зависимостей
```bash
pip install -r requirements.txt
```

4. Настройка переменных окружения
Создайте файл .env в корне проекта и добавьте следующие переменные:

```env
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/todo_app
SECRET_KEY=your-secret-key
REFRESH_TOKEN_SECRET_KEY=your-refresh-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=14400
```

5. Применение миграций
```bash
alembic upgrade head
```

6. Запуск приложения
```bash
uvicorn app.main:app --reload
```
API будет доступно по адресу: http://127.0.0.1:8000.

7. Документация API
FastAPI автоматически генерирует документацию:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

8. Тестирование
Для запуска тестов выполните:

```bash
pytest
```

## Запуск в Docker

1. Настройка переменных окружения
Создайте файл .env в корне проекта и добавьте следующие переменные:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db/todo_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440
```

2. Применение миграций
```bash
docker compose run web alembic upgrade head
```

3. Запуск
```bash
docker compose up
```
