from fastapi import APIRouter
from .routes import asignaciones_router

asignaciones_sub_router = APIRouter(
    prefix="/asignaciones",
    tags=["Asignaciones"],
)

asignaciones_sub_router.include_router(
    asignaciones_router
)
