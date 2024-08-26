from fastapi import APIRouter

from .tareas import tareas_sub_router
from .auth import auth_sub_router
from .mail import mail_sub_router
from .molde import molde_sub_router
from .usuarios import user_sub_router
from .account import account_sub_router
from .clientes import clientes_sub_router
from .asignaciones import asignaciones_sub_router

router = APIRouter()

router.include_router(
    auth_sub_router,
)

router.include_router(
    account_sub_router,
)

router.include_router(
    molde_sub_router
)

router.include_router(
    user_sub_router,
)

router.include_router(
    clientes_sub_router,
)

router.include_router(
    tareas_sub_router
)

router.include_router(
    asignaciones_sub_router
)

router.include_router(
    mail_sub_router,
)

__all__ = ["router"]
