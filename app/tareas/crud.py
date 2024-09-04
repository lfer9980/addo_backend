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
from app.models.asignacion import AsignacionModel
from app.asignaciones.crud import AsignacionCRUD
from app.clientes.crud import ClienteCRUD

from core.utils.calculate_cargas_trabajo import CargasCalc


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
        
        usuario = usuario_query.first()
        
        usuario_exists = True if usuario is not None else False
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
        
        return usuario
        
            

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
        
        tarea_complejidad = data["complejidad"]
        
        new_tcve = await CargasCalc.calculate_tcve(tareas=cliente.tareas,
                                                   new_tarea=tarea_complejidad
                                                   )
        
        ct = await CargasCalc.calculate_ct(cte=tarea_complejidad,
                                           tcve=new_tcve,
                                           ce=cliente.complejidad
                                           )
        
        data["carga_trabajo"] = ct
 
        data = await cls._create(db, data)
        
        info_tarea = data.model_dump()
        
        tarea_id = data.id

        data_asignacion = {
            'tarea_id': tarea_id,
            'username': username,
            'estado': EstadoAsignacionEnum.Progreso,
        }

        asignacion = await AsignacionCRUD.create_asignacion(db, data=data_asignacion)
        info_asignacion = asignacion.model_dump()
    
        tmp_data = {**info_asignacion, **info_tarea}
        
        await cls.update_tcve(db=db, rfc=cliente.rfc, tcve=new_tcve)

        return TareaResponse.model_validate(tmp_data)

    @classmethod
    async def update(cls, db: Session, 
                     data: UpdateTareaSchema,
                     tarea_id: str, 
                     username:str) -> TareaSchema:
        
        tcve = 0
        
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

        await AsignacionCRUD.update_asignacion(db=db,
                                               tarea_id=tarea_id,
                                               nuevo_usuario_username=user,
                                               )
        
        data_complejidad = data["complejidad"]
        
        if old_tarea["complejidad"] is not data_complejidad:
            cliente = old_tarea.cliente
            tcve = CargasCalc.calculate_tcve(tareas=cliente.tareas)
            
            await cls.update_tcve(tcve=tcve)

        return TareaSchema.model_validate(old_tarea)

    @classmethod
    async def delete(cls, db: Session, tarea_id: str):

        tarea = await cls._get_one(db=db,
                                   table=cls.current_table,
                                   this_id=tarea_id)
        
        cliente = tarea.cliente

        await AsignacionCRUD.delete_asignacion(db=db, tarea_id=tarea_id)
        
        await cls._delete(db=db, data=tarea)
        
        new_tcve = await CargasCalc.calculate_tcve(tareas=cliente.tareas)
        
        await cls.recalculate_all_ct(db=db, 
                                     tcve=new_tcve,
                                     tareas=cliente.tareas,
                                     cliente=cliente)
        

    @classmethod
    async def get_all(cls, db: Session, page: int = 1, page_size: int = 10) -> List[TareaGetAllSchema]:
       
        tareas = await cls._get_all(db=db,
                                    table=cls.current_table,
                                    page=page,
                                    page_size=page_size)      
                               
        tareas_list = [{**tarea.to_dict(), 
                        **tarea.asignacion.to_dict(),
                        "id": tarea.to_dict()["id"],
                        "razon_social": tarea.cliente.to_dict()["razon_social"]} 
                       for tarea in tareas]
        
        return [TareaGetAllSchema.model_validate(tarea) for tarea in tareas_list]

    @classmethod
    async def get_by_user(cls, db: Session, username: str, page: int = 1, page_size: int = 10) -> List[TareaGetUserSchema]:
        
        usuario = await cls._validate_usuario(db, username=username)
        
        tareas_list = [{**asignacion.to_dict(), 
                        **asignacion.tarea.to_dict(),
                        "id": asignacion.tarea.to_dict()["id"],
                        "razon_social": asignacion.tarea.cliente.to_dict()["razon_social"]} 
                       for asignacion in usuario.asignaciones]
        
        return [TareaGetUserSchema.model_validate(tarea) for tarea in tareas_list]

    @classmethod
    async def get_by_client(cls, db: Session, rfc: str) -> List[TareaGetClientSchema]:
        
        cliente = await cls._validate_cliente(db=db, rfc=rfc)
        
        tareas_list = [{**tarea.to_dict(), 
                        **tarea.asignacion.to_dict(),
                        "id": tarea.to_dict()["id"],} 
                       for tarea in cliente.tareas]
        
        return [TareaGetClientSchema.model_validate(tarea) for tarea in tareas_list]
    
    @classmethod
    async def update_tcve(cls, db: Session, rfc: str, tcve: float | None = None):
        
        new_tcve:float 
        
        cliente_query: Query = await cls._filter_by(db=db,
                                                    table=ClienteModel,
                                                    key='rfc',
                                                    data=rfc)
            
        cliente = cliente_query.first()
        
        if tcve is None: 
            new_tcve = await CargasCalc.calculate_tcve(tareas=cliente.tareas)
        else: 
            new_tcve = tcve     
        
        cliente.tcve = new_tcve
        
        await cls._update(db=db, data=cliente)
        
        return new_tcve
    
    
    @classmethod
    async def recalculate_all_ct(cls, db: Session, tcve: float, tareas: list[int], cliente: ClienteModel): 
        
        tareas_list = [tarea.to_dict() for tarea in tareas]   
        
        cliente = cliente.to_dict()
         
        new_ct_tareas_list = [{**tarea, 
                               "carga_trabajo": await CargasCalc.calculate_ct(cte=tarea["complejidad"], tcve=tcve,ce=cliente["complejidad"])  
                               }
                              for tarea in tareas_list]
        
        
        for ct_update in new_ct_tareas_list:
            print(ct_update)
                
        