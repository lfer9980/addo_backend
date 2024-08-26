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

    usuario_asignado: str | None = tarea_dict.get('username', None)

    if usuario_asignado is None:
        raise HTTPException(
            status_code=400,
            detail='usuario asignado requerido en el campo...'
        )

    CreateTareaSchema.model_validate(tarea_dict)

    return await TareasCRUD.create(db=db, data=tarea, rfc=rfc.upper(), username=usuario_asignado)


@tareas_router.put('/update/{tarea_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def update_tarea(tarea_id: str,
                       tarea: UpdateTareaSchema,
                       db: Session = Depends(create_session),
                       current_session: Depends = Depends(Manager)):
    
    tarea_dict = tarea.model_dump()
    print()

    usuario_asignado: str | None = tarea_dict.get('username', None)

    if usuario_asignado is None:
        raise HTTPException(
            status_code=400,
            detail='usuario asignado requerido en el campo...'
        )

    return await TareasCRUD.update(db=db, data=tarea, tarea_id=tarea_id, username=usuario_asignado)


@tareas_router.delete('/delete/{tarea_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def delete_tarea(tarea_id: str,
                         db: Session = Depends(create_session),
                         current_session: Depends = Depends(Manager)):

    await TareasCRUD.delete(db=db, tarea_id=tarea_id)
    return {'message': f'Tarea {tarea_id} eliminada correctamente'}


@tareas_router.get('/get/all/{page}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_all_tareas(page: int = 1,
                         db: Session = Depends(create_session),
                         current_session: Depends = Depends(Manager)):
    
    return await TareasCRUD.get_all(db=db, page=page)


@tareas_router.get('/get/user/{username}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_tarea_by_user(username: str,
                            page: int = 1,        
                            db: Session = Depends(create_session),
                            current_session: Depends = Depends(Manager)):
    
    return await TareasCRUD.get_by_user(db=db, 
                                        page=page,
                                        username=username)


@tareas_router.get('/get/client/{rfc}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def get_tarea_by_client(rfc: str,
                              page: int = 1,
                              db: Session = Depends(create_session),
                              current_session: Depends = Depends(Manager)):
    
    return await TareasCRUD.get_by_client(db=db,
                                          page=page,
                                          rfc=rfc)