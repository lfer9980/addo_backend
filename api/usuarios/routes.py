from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.db import create_session
from app.usuarios.schemas import *
from app.usuarios.crud import UserCRUD
from core.utils.token import Manager
from app.usuarios.enums import UserTypeEnum

from app.usuarios.permissions import can_access

user_router = APIRouter()


@user_router.post('/create')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def create_user(user: CreateUserSchema,
                      current_session: Depends = Depends(Manager),
                      db: Session = Depends(create_session),
                      ) -> BaseUserSchema:

    CreateUserSchema.model_validate(user)

    return await UserCRUD().create(user=user, db=db)


@user_router.put('/update/{user_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def update_user(user_id: str,
                      user_data: UpdateUserSchema,
                      current_session: Depends = Depends(Manager),
                      db: Session = Depends(create_session)):

    user_session_id: str = current_session.get('id')

    UpdateUserSchema.model_validate(user_data)
    print("validado")

    return await UserCRUD().update_user(
        db=db,
        user_update_id=user_id,
        user_updating_id=user_session_id,
        user=user_data
    )


@user_router.delete('/delete/{user_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador, UserTypeEnum.Supervisor])
async def delete_user(user_id: str,
                      current_session: Depends = Depends(Manager),
                      db: Session = Depends(create_session)):

    await UserCRUD().delete(
        db=db,
        user_id=user_id
    )

    return {"message": f"Usuario {user_id} eliminado correctamente"}


@user_router.get('/get/all/{page}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_all(page: int,
                  db: Session = Depends(create_session),
                  current_session: Depends = Depends(Manager)) -> List[UserSchema]:

    return await UserCRUD().get_all(db=db,
                                    page=page,
                                    page_size=10)


@user_router.get('/get/{user_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_user(user_id: str,
                   db: Session = Depends(create_session),
                   current_session: Depends = Depends(Manager)) -> UserSchema:

    return await UserCRUD().get_one(db=db,
                                    user_id=user_id)
