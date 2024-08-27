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

    return await UserCRUD.create(user=user, db=db)


@user_router.put('/update/{username}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def update_user(username: str,
                      user_data: UpdateUserSchema,
                      current_session: Depends = Depends(Manager),
                      db: Session = Depends(create_session)):

    user_username: str = current_session.get('username')

    UpdateUserSchema.model_validate(user_data)

    return await UserCRUD.update_user(db=db,
                                      user_update_username=username,
                                      user_updating_username=user_username,
                                      user=user_data
                                      )


@user_router.delete('/delete/{username}')
@can_access(not_allowed=[UserTypeEnum.Colaborador, UserTypeEnum.Supervisor])
async def delete_user(username: str,
                      current_session: Depends = Depends(Manager),
                      db: Session = Depends(create_session)):

    await UserCRUD.delete(db=db, username=username)

    return {"message": f"Usuario {username} eliminado correctamente"}


@user_router.get('/get/all/{page}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_all_users(page: int,
                  db: Session = Depends(create_session),
                  current_session: Depends = Depends(Manager)) -> List[UserSchema]:

    return await UserCRUD.get_all(db=db,
                                    page=page,
                                    page_size=50)


@user_router.get('/get/{username}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_user_by_username(username: str,
                   db: Session = Depends(create_session),
                   current_session: Depends = Depends(Manager)) -> UserSchema:

    return await UserCRUD.get_one(db=db,
                                  username=username)
