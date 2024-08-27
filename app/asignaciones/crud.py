import pytz
from typing import List
from datetime import datetime

from aiosmtplib import status
from fastapi import HTTPException
from sqlalchemy.orm import Session, Query

from core.db import BaseCRUD
from app.asignaciones.schemas import *

from app.models import TareaModel
from app.models import AsignacionModel
from app.models import UsuarioModel

class AsignacionCRUD(BaseCRUD):
    current_table = AsignacionModel

    @classmethod
    async def _validate_tarea(cls, db: Session, tarea_id: str):
        tarea = await cls._exist(db,
                                 table=TareaModel,
                                 this_id=tarea_id)

        if not tarea:
            raise HTTPException(
                status_code=404,
                detail='La tarea seleccionada no existe',
            )

    @classmethod
    async def _validate_usuario(cls, db: Session, username: str):
        usuario_check = db.query(UsuarioModel).where(
            getattr(UsuarioModel, 'username') == username
        )
        
        usuario_exists = True if usuario_check.first() is not None else False
    
        if not usuario_exists:
            raise HTTPException(
                status_code=404,
                detail='El usuario ingresado es no valido...',
            )


    @classmethod
    async def _create(cls, db: Session, data: dict) -> AsignacionBase:
        db_asignacion = AsignacionModel(**data)

        await cls._save(db, db_asignacion)
        return AsignacionBase.model_validate(db_asignacion)

    @classmethod
    async def create_asignacion(cls, db: Session, data: dict) -> AsignacionResponse:

        parse_data: AsignacionCreate = AsignacionCreate.model_validate(data)

        await cls._validate_tarea(db, parse_data.tarea_id)

        data = await cls._create(db, data)

        user: Query = await cls._filter_by(db=db,
                                           table=UsuarioModel,
                                           key='username',
                                           data=parse_data.username)

        user: UsuarioModel = user.first()
        data = AsignacionBase.model_dump(data)
        data['username'] = user.username

        return AsignacionResponse.model_validate(data)

    @classmethod
    async def delete_asignacion(cls, db: Session, tarea_id: str) -> None:

        this_tarea: Query = await cls._filter_by(db=db,
                                                 table=cls.current_table,
                                                 key='tarea_id',
                                                 data=tarea_id)

        this_tarea = this_tarea.first()
        print(this_tarea)

        if not this_tarea:
            raise HTTPException(
                status_code=404,
                detail='No fue posible eliminar la asignacion...',
            )
            
        await cls._delete(db, this_tarea)


    @classmethod
    async def update_asignacion(cls, db: Session, tarea_id: str, nuevo_usuario_username: str) -> AsignacionBase:

        await cls._validate_usuario(db, username=nuevo_usuario_username)
        await cls._validate_tarea(db, tarea_id=tarea_id)

        this_asignacion_id: Query = await cls._filter_by(db=db,
                                                         table=cls.current_table, 
                                                         key='tarea_id',
                                                         data=tarea_id)

        this_asignacion: AsignacionModel | None = this_asignacion_id.filter(
            AsignacionModel.completado == False 
        ).first()

        if this_asignacion is None:
            data_asignacion = {
                'tarea_id': tarea_id,
                'username': nuevo_usuario_username,
                'estado': EstadoAsignacionEnum.Progreso, 
                'ultimo_cambio': datetime.now(pytz.timezone('Etc/GMT+6'))
            }
            
            data_asignacion = await cls._create(db, data_asignacion)

            user: Query = await cls._filter_by(db=db,
                                            table=UsuarioModel,
                                            key='username',
                                            data=nuevo_usuario_username)

            user: UsuarioModel = user.first()
            this_asignacion.username = user.username
    
        else:
            this_asignacion.username = nuevo_usuario_username
            this_asignacion.ultimo_cambio = datetime.now(pytz.timezone('Etc/GMT+6'))
            
        
        await cls._update(db, this_asignacion)

        return AsignacionResponse.model_validate(this_asignacion)

    @classmethod
    async def completar_asignacion(cls, db: Session, tarea_id: str) -> AsignacionBase:

        asignacion_query = await cls._filter_by(db=db,
                                                table=cls.current_table,
                                                key='tarea_id',
                                                data=tarea_id)
        
        asignacion: AsignacionModel = asignacion_query.first()

        if asignacion.completado:
            raise HTTPException(
                status_code=404,
                detail='Esta tarea ya fue completada'
            )

        asignacion.completado = True
        asignacion.terminado = datetime.now(pytz.timezone('Etc/GMT+6'))
        
        await cls._save(db, asignacion)  
        
        return AsignacionResponse.model_validate(asignacion)

    
    @classmethod
    async def estado_asignacion(cls, db: Session, tarea_id: str, nuevo_estado: str) -> AsignacionBase:
        
        asignacion_query = await cls._filter_by(db=db,
                                                table=cls.current_table,
                                                key='tarea_id',
                                                data=tarea_id)
        
        asignacion: AsignacionModel = asignacion_query.first()

        if not asignacion:
            raise HTTPException(
                status_code=404,
                detail=f'La asignacion de la tarea: {tarea_id} seleccionado no existe',
            )
        
        asignacion.estado = nuevo_estado
        asignacion.ultimo_cambio = datetime.now(pytz.timezone('Etc/GMT+6'))
      
        await cls._save(db, asignacion)
        
        return AsignacionResponse.model_validate(asignacion)
    
    @classmethod
    async def get_one(cls, db: Session, tarea_id: str) -> None:
        
        asignacion_query = await cls._filter_by(db=db,
                                             table=AsignacionModel,
                                             key='tarea_id',
                                             data=tarea_id)

        asignacion = asignacion_query.first()

        if not asignacion:
            raise HTTPException(
                status_code=404,
                detail=f'La asignacion de la tarea: {tarea_id} seleccionado no existe',
            )

        return asignacion
            
    @classmethod
    async def get_all(cls, db: Session, page: int = 1, page_size: int = 10) -> List[AsignacionBase]:
        
        asignaciones = await cls._get_all(db=db,
                                          table=AsignacionModel,
                                          page=page,
                                          page_size=page_size)        

        return [AsignacionBase.model_validate(asignacion) for asignacion in asignaciones]


        