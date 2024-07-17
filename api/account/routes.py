from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from sqlalchemy.sql.functions import current_user

from core.db import create_session
from app.usuarios.schemas import *
from app.usuarios.crud import UserCRUD
from core.utils.token import Manager


account_router = APIRouter()


@account_router.get('/get')
async def get_current(current_session=Depends(Manager)) -> UserSchema:
    return UserSchema.model_validate(current_session)


@account_router.put('/update')
async def update(user_data: UpdateOwnUserSchema,
                 current_session=Depends(Manager),
                 db: Session = Depends(create_session)) -> UserSchema:

    user_id = current_session.get('id')
    UpdateOwnUserSchema.model_validate(user_data)

    return await UserCRUD.update_me(
        db=db,
        user_id=user_id,
        user=user_data
    )


@account_router.get('/delete')
async def delete(current_session=Depends(Manager),
                 db: Session = Depends(create_session)) -> UserSchema:

    user_id = current_session.get('id')
    await UserCRUD.delete(db=db,
                          user_id=user_id)

    return current_session
