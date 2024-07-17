from fastapi import APIRouter

from .routes import clientes_router

clientes_sub_router = APIRouter(
    prefix="/clientes",
    tags=["clientes"],
)

clientes_sub_router.include_router(
    clientes_router
)
