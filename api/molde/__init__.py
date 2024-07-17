from fastapi import APIRouter
from .routes import molde_router

molde_sub_router = APIRouter(
    prefix="/molde",
    tags=["Molde"],
)

molde_sub_router.include_router(
    molde_router
)
