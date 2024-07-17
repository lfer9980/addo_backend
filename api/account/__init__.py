from fastapi import APIRouter

from .routes import account_router

account_sub_router = APIRouter(
    prefix="/account",
    tags=["account"],
)

account_sub_router.include_router(
    account_router
)
