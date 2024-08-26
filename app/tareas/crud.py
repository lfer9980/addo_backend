from operator import or_
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session, Query
from fastapi import HTTPException

from core.db import BaseCRUD
from app.tareas.schemas import *
from app.asignaciones.enums import *

from app.models import ClienteModel, UsuarioModel
from app.models.tareas import TareaModel
from app.asignaciones.crud import AsignacionCRUD
from app.clientes.crud import ClienteCRUD


class TareasCRUD(BaseCRUD):
    current_table = TareaModel

    @classmethod
    async def _validate_cliente(cls, db: Session, rfc: str) -> ClienteModel:

        cliente_query = await cls._filter_by(db=db,
                                             table=ClienteModel,
                                             key='rfc',
                                             data=rfc)

        cliente = cliente_query.first()

        if not cliente:
            raise HTTPException(
                status_code=404,
                detail='El cliente seleccionado no existe',
            )

        return cliente

    @classmethod
    async def _validate_usuario(cls, db: Session, username: str):
        usuario_query = db.query(UsuarioModel).where(
            getattr(UsuarioModel, 'username') == username
        )
        
        usuario_exists = True if usuario_query.first() is not None else False
        usuario_super = True if username == "superuser" else False
    
        if not usuario_exists:
            raise HTTPException(
                status_code=404,
                detail='El usuario ingresado es no valido...',
            )
        
        if usuario_super:
            raise HTTPException(
                status_code=404,
                detail='No es posible asignar tareas al super usuario...',
            )
        
            

    @classmethod
    async def _create(cls, db: Session, data: dict) -> TareaSchema:

        db_tarea = TareaModel(**data)

        await cls._save(db=db, data=db_tarea)

        return TareaSchema.model_validate(db_tarea)

    @classmethod
    async def create(cls, db: Session, data: CreateTareaSchema, rfc: str, username: str) -> TareaResponse:

        cliente = await cls._validate_cliente(db, rfc)
        await cls._validate_usuario(db, username=username)

        data = data.model_dump()
        data['cliente_rfc'] = cliente.rfc
        data.pop('username')

        data = await cls._create(db, data)
        
        tarea_id = data.id

        data_asignacion = {
            'tarea_id': tarea_id,
            'username': username,
            'estado': EstadoAsignacionEnum.Progreso,
        }

        info_asignacion = await AsignacionCRUD.create_asignacion(db, data=data_asignacion)
        
        info_tarea = data.model_dump()
    
        tmp_data = {**info_asignacion.model_dump(), **info_tarea}

        return TareaResponse.model_validate(tmp_data)

    @classmethod
    async def update(cls, db: Session, 
                     data: UpdateTareaSchema,
                     tarea_id: str, 
                     username:str) -> TareaSchema:
        
        await cls._validate_usuario(db, username=username)

        old_tarea: Query = await cls._get_one(db=db,
                                              table=cls.current_table,
                                              this_id=tarea_id)
        
        if old_tarea is None:
            raise HTTPException(
                status_code=404,
                detail=f"Tarea no encontrada: {tarea_id}"
            )

        data = data.model_dump()

        user = data.pop('username')

        for key, value in data.items():
            if value is not None:
                setattr(old_tarea, key, value)

        await cls._update(db=db, data=old_tarea)

        await AsignacionCRUD.update_asignacion(
            db=db,
            tarea_id=tarea_id,
            nuevo_usuario_username=user
        )

        return TareaSchema.model_validate(old_tarea)

    @classmethod
    async def delete(cls, db: Session, tarea_id: str):

        tarea = await cls._get_one(db=db,
                                   table=cls.current_table,
                                   this_id=tarea_id)

        await AsignacionCRUD.delete_asignacion(db=db, tarea_id=tarea_id)

        await cls._delete(db=db, data=tarea)

    @classmethod
    async def get_all(cls, db: Session, page: int = 1, page_size: int = 10) -> List[TareaGetAllSchema]:
       
        tareas = await cls._get_all(db=db,
                                    table=cls.current_table,
                                    page=page,
                                    page_size=page_size)        

        asignaciones = await AsignacionCRUD.get_all(db=db,
                                                    page=page,
                                                    page_size=page_size)
        


        tareas_list = [tarea.to_dict() for tarea in tareas]
        asignaciones_dict = {asignacion.model_dump()["tarea_id"]: asignacion.model_dump() for asignacion in asignaciones}

        tareas_asignaciones = []
        
        for item in tareas_list:
            cliente_data = await ClienteCRUD.get_one_by_id(db=db,
                                                           cliente_id=item.get("cliente_id"))
            
            cliente_data = cliente_data.model_dump()
            
            if item["id"] in asignaciones_dict:
                merged_item = {**item, **asignaciones_dict[item["id"]], **cliente_data}
                
            else:
                 merged_item = {**item, **cliente_data}
            
            tareas_asignaciones.append(merged_item)

        return [TareaGetAllSchema.model_validate(tarea) for tarea in tareas_asignaciones]

    @classmethod
    async def get_by_user(cls, db: Session, username: str, page: int = 1, page_size: int = 10) -> List[TareaGetUserSchema]:
        
        await cls._validate_usuario(db, username=username)
        
        asignaciones = await AsignacionCRUD.get_all_by_key(db=db, 
                                                           key="username",
                                                           data=username,
                                                           page=page,
                                                           page_size=page_size)
        
        asignaciones_list = [asignacion.model_dump() for asignacion in asignaciones]

        tareas_asignaciones = []
        
        for item in asignaciones_list:
            tarea_data = await cls._get_one(db=db,
                                table=cls.current_table,
                                this_id=item.get("tarea_id"))
            
            tarea_data = tarea_data.to_dict()
            
            cliente_data = await ClienteCRUD.get_one_by_id(db=db,
                                                           cliente_id=tarea_data.get("cliente_id"))
            
            cliente_data = cliente_data.model_dump()
            
            merged_item = {**item, **tarea_data, **cliente_data}
            tareas_asignaciones.append(merged_item)
        
        return [TareaGetUserSchema.model_validate(tarea) for tarea in tareas_asignaciones]
    
    @classmethod
    async def get_by_client(cls, db: Session, rfc: str, page: int = 1, page_size: int = 10):
        
        cliente = await cls._validate_cliente(db=db,
                                              rfc=rfc)
    
        return cliente.tareas
        
        
        
