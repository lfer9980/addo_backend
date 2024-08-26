from fastapi import status
from functools import wraps
from fastapi.exceptions import HTTPException


def can_access(not_allowed: list = ()):

    def decorator(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            session: dict | None = kwargs.get("current_session", None)
            if session is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No session has been established",
                )

            tipo_usuario = session.get('tipo_usuario', None)

            if tipo_usuario is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='No user type found',
                )

            elif tipo_usuario and tipo_usuario in not_allowed:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Not enough permissions',
                )

            return await function(*args, **kwargs)

        return wrapper

    return decorator
