from fastapi import APIRouter
from .routes import mail_router

mail_sub_router = APIRouter(
    prefix="/mail",
    tags=["Mail"],
)

mail_sub_router.include_router(
    mail_router
)
