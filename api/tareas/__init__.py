from fastapi import APIRouter
from .routes import tareas_router

tareas_sub_router = APIRouter(
    prefix="/tareas",
    tags=["Tareas"],
)

tareas_sub_router.include_router(
    tareas_router
)
