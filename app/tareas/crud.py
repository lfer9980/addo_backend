from operator import or_
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session, Query
from fastapi import HTTPException

from core.db import BaseCRUD
from app.tareas.schemas import *

from app.models import ClienteModel, AsignacionModel
from app.models.tareas import TareaModel
from app.asignaciones.crud import AsignacionCRUD


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
    async def _create(cls, db: Session, data: dict) -> TareaSchema:

        db_tarea = TareaModel(**data)

        await cls._save(db=db, data=db_tarea)

        return TareaSchema.model_validate(db_tarea)

    @classmethod
    async def create(cls, db: Session, data: CreateTareaSchema, rfc: str) -> TareaResponse:

        cliente = await cls._validate_cliente(db, rfc)

        data = data.model_dump()
        data['cliente_id'] = cliente.id
        usuario_id = data.pop('usuario_id')

        data = await cls._create(db, data)

        tarea_id = data.id

        data_asignacion = {
            'tarea_id': tarea_id,
            'usuario_id': usuario_id,
            'completado': False,

        }

        info_asignacion = await AsignacionCRUD.create(db, data=data_asignacion)
        info_tarea = data.model_dump()

        tmp_data = {**info_asignacion.model_dump(), **info_tarea}

        return TareaResponse.model_validate(tmp_data)

    @classmethod
    async def update(cls, db: Session, data: UpdateTareaSchema,
                     tarea_id: str) -> TareaSchema:

        old_tarea: TareaModel = await cls._get_one(db=db,
                                                   table=cls.current_table,
                                                   this_id=tarea_id)

        old_tarea: dict = UpdateTareaSchema.model_dump(old_tarea) # noqa

        data = data.model_dump()

        usuario_id = data.pop('usuario_id')

        for key, value in data.items():
            if value is not None:
                setattr(old_tarea, key, value)

        await cls._update(db=db, data=old_tarea)

        await AsignacionCRUD.reasignar(
            db=db,
            tarea_id=tarea_id,
            nuevo_usuario_id=usuario_id
        )

        return TareaSchema.model_validate(old_tarea)

    @classmethod
    async def delete(cls, db: Session, tarea_id: str):

        tarea = await cls._get_one(db=db,
                                   table=cls.current_table,
                                   this_id=tarea_id)

        await AsignacionCRUD.delete(db=db, tarea_id=tarea_id)

        await cls._delete(db=db, data=tarea)

    @classmethod
    async def get_all(cls, db: Session, page: int = 1, page_size: int = 10) -> List[TareaSchema]:
        tareas = await cls._get_all(db=db,
                                    table=cls.current_table,
                                    page=page,
                                    page_size=page_size)

        return [TareaSchema.model_validate(tarea) for tarea in tareas]
