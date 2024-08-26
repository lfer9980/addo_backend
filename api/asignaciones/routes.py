from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from app.asignaciones.schemas import *
from app.asignaciones.crud import *
from core.db import create_session
from core.utils.token import Manager
from app.usuarios.enums import UserTypeEnum
from app.usuarios.permissions import can_access


asignaciones_router = APIRouter()


@asignaciones_router.put('/reasignar/{tarea_id}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def update_asignacion(tarea_id: str,
                            nuevo_usuario_username: str,
                            db: Session = Depends(create_session),
                            current_session: Depends = Depends(Manager)):

    return await AsignacionCRUD.update_asignacion(db=db,
                                              tarea_id=tarea_id,
                                              nuevo_usuario_username=nuevo_usuario_username)
    
    
@asignaciones_router.put('/estado/{tarea_id}')
async def cambiar_estado_asignacion(tarea_id: str,
                         nuevo_estado: EstadoAsignacionEnum,
                         db: Session = Depends(create_session),
                         current_session: Depends = Depends(Manager)):

    return await AsignacionCRUD.estado_asignacion(db=db,
                                              tarea_id=tarea_id,
                                              nuevo_estado=nuevo_estado)
    
@asignaciones_router.put('/completar/{tarea_id}')
async def completar_asignacion(tarea_id: str,
                               db: Session = Depends(create_session),
                               current_session: Depends = Depends(Manager)):

    return await AsignacionCRUD.completar_asignacion(db=db,
                                                     tarea_id=tarea_id)