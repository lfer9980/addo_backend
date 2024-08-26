from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.db import create_session
from core.utils.token import Manager
from app.tareas_estandar.schemas import *
from app.usuarios.enums import UserTypeEnum
from app.tareas_estandar.crud import TareaEstandarCRUD

from app.usuarios.permissions import can_access


molde_router = APIRouter()


@molde_router.post('/create')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def create_molde(molde: CreateTareaEstandarSchema,
                       db: Session = Depends(create_session),
                       current_session: Depends = Depends(Manager)) -> TareaEstandarSchema:

    CreateTareaEstandarSchema.model_validate(molde)

    return await TareaEstandarCRUD.create(db=db,
                                          tarea=molde)


@molde_router.put('/update/{molde_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def update_molde(molde_id: str,
                       molde: UpdateTareaEstandarSchema,
                       db: Session = Depends(create_session),
                       current_session: Depends = Depends(Manager)):

    UpdateTareaEstandarSchema.model_validate(molde)
    return await TareaEstandarCRUD.update(db=db,
                                          tarea_id=molde_id,
                                          tarea=molde)


@molde_router.delete('/delete/{molde_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def delete_molde(molde_id: str,
                         db: Session = Depends(create_session),
                         current_session: Depends = Depends(Manager)):

    await TareaEstandarCRUD.delete(db=db,
                                   tarea_id=molde_id)

    return {"message": f"Tarea con ID:{molde_id} eliminado correctamente"}


@molde_router.get('/get/all/{page}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_all_molde(page: int,
                  db: Session = Depends(create_session),
                  current_session: Depends = Depends(Manager)):

    return await TareaEstandarCRUD().get_all(db=db,
                                             page=page,
                                             page_size=10)


@molde_router.get('/get/{molde_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_molde_by_id(molde_id: str,
                    db: Session = Depends(create_session),
                    current_session: Depends = Depends(Manager)) -> TareaEstandarSchema:

    return await TareaEstandarCRUD.get_one(db=db,
                                           tarea_id=molde_id)
