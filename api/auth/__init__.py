from fastapi import APIRouter

from .routes import auth_router

auth_sub_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

auth_sub_router.include_router(
    auth_router
)
