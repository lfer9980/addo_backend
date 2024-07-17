from fastapi import APIRouter
from .routes import user_router

user_sub_router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"],
)

user_sub_router.include_router(
    user_router
)
