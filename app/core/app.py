from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.api import router as auth_router
from app.categories.api import router as categories_router
from app.tasks.api import router as tasks_router
from app.users.api import router as users_router


def create_app():
    app = FastAPI()

    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_credentials=True, allow_headers=["*"])

    app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
    app.include_router(tasks_router, prefix="/api/v1", tags=["tasks"])
    app.include_router(categories_router, prefix="/api/v1", tags=["categories"])
    app.include_router(users_router, prefix="/api/v1", tags=["users"])
    return app
