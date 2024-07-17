from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.tareas.schemas import *
from core.db import create_session
from core.utils.token import Manager
from app.tareas.crud import TareasCRUD
from app.usuarios.enums import UserTypeEnum
from app.usuarios.permissions import can_access


tareas_router = APIRouter()


@tareas_router.post('/create/{rfc}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def create_tarea(rfc: str,
                       tarea: CreateTareaSchema,
                       db: Session = Depends(create_session),
                       current_session: Depends = Depends(Manager)):

    tarea_dict = tarea.model_dump()

    id_usuario_asignado: str | None = tarea_dict.get('usuario_id', None)

    if id_usuario_asignado is None:
        raise HTTPException(
            status_code=400,
            detail='id_usuario requerido'
        )

    CreateTareaSchema.model_validate(tarea_dict)

    return await TareasCRUD.create(db=db, data=tarea, rfc=rfc.upper())


@tareas_router.put('/update/{tarea_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def update_tarea(tarea_id: str,
                       db: Session = Depends(create_session),
                       current_session: Depends = Depends(Manager)):
    return {'message': 'Not implemented yet'}


@tareas_router.delete('/delete/{tarea_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def delete_cliente(tarea_id: str,
                         db: Session = Depends(create_session),
                         current_session: Depends = Depends(Manager)):

    await TareasCRUD.delete(db=db, tarea_id=tarea_id)
    return {'message': f'Tarea {tarea_id} eliminada correctamente'}


@tareas_router.get('/get/all/{page}/{page_size}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_all(page: int = 1,
                  page_size: int = 10,
                  db: Session = Depends(create_session),
                  current_session: Depends = Depends(Manager)):
    return await TareasCRUD.get_all(db=db, page=page, page_size=page_size)


@tareas_router.get('/get/user/{user_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_by_user(user_id: str,
                      db: Session = Depends(create_session),
                      current_session: Depends = Depends(Manager)):
    return {'message': 'Not implemented yet'}


@tareas_router.get('/get/client/{client_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_by_user(client_id: str,
                      db: Session = Depends(create_session),
                      current_session: Depends = Depends(Manager)):
    return {'message': 'Not implemented yet'}
