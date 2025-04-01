# To-Do App API

To-Do App API — это RESTful веб-сервис, который позволяет пользователям управлять задачами (tasks), категориями (categories) и профилями пользователей (users). Проект использует FastAPI, SQLAlchemy и JWT для аутентификации.

## Установка и запуск
1. Клонирование репозитория
```bash
git clone https://github.com/g1n-ru/todo.git
```

2. Настройка переменных окружения
Создайте файл .env в корне проекта и добавьте следующие переменные:

```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db/todo_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=1440
```

3. Запуск приложения
```bash
docker compose up
```

4. Применение миграций (только после первого запуска)
```bash
docker compose run web alembic upgrade head
```
5. Запуск тестов
```bash
docker compose run web pytest
```

## Подробности эксплуатации API
- API будет доступно по адресу: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc