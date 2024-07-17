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
    async def _validate_usuario(cls, db: Session, user_id: str):
        usuario = await cls._exist(db,
                                   table=UsuarioModel,
                                   this_id=user_id)

        if not usuario:
            raise HTTPException(
                status_code=404,
                detail='El usuario seleccionado no existe',
            )

    @classmethod
    async def _create(cls, db: Session, data: dict) -> AsignacionBase:
        db_asignacion = AsignacionModel(**data)

        await cls._save(db, db_asignacion)
        return AsignacionBase.model_validate(db_asignacion)

    @classmethod
    async def create(cls, db: Session, data: dict) -> AsignacionResponse:

        parse_data: AsignacionCreate = AsignacionCreate.model_validate(data)

        await cls._validate_usuario(db, parse_data.usuario_id)
        await cls._validate_tarea(db, parse_data.tarea_id)

        data = await cls._create(db, data)

        user: Query = await cls._filter_by(db=db,
                                           table=UsuarioModel,
                                           key='id',
                                           data=parse_data.usuario_id)

        user: UsuarioModel = user.first()
        data = AsignacionBase.model_dump(data)
        data['username'] = user.username

        return AsignacionResponse.model_validate(data)

    @classmethod
    async def delete(cls, db: Session, tarea_id: str) -> None:

        this_tarea: Query = await cls._filter_by(db=db,
                                                 table=TareaModel,
                                                 key='id',
                                                 data=tarea_id)

        if this_tarea.first():
            await cls._delete(db, this_tarea.first())

    @classmethod
    async def reasignar(cls, db: Session, tarea_id: str, nuevo_usuario_id: str) -> AsignacionBase:

        await cls._validate_usuario(db, nuevo_usuario_id)

        this_id_tarea: Query = await cls._filter_by(db=db,
                                                    table=TareaModel,
                                                    key='id_tarea',
                                                    data=tarea_id)

        this_tarea: TareaModel | None = this_id_tarea.filter(
            AsignacionModel.completado == False  # noqa
        ).first()

        if this_tarea is None:
            raise HTTPException(
                status_code=404,
                detail='Esta tarea no puede ser reasignada'
            )

        this_tarea.user_id = nuevo_usuario_id

        await cls._update(db, this_tarea)

        return AsignacionBase.model_validate(this_tarea)

    @classmethod
    async def completar(cls, db: Session, asignacion_id: str) -> AsignacionBase:

        asignacion = await cls._get_one(db, table=AsignacionModel, this_id=asignacion_id)

        if asignacion['completado']:
            raise HTTPException(
                status_code=404,
                detail='Esta tarea ya fue completada'
            )

        asignacion['completado'] = True
        asignacion['finished_at'] = datetime.now()
        await cls._save(db, asignacion)

        nueva_asignacion = {
            'cliente_id': asignacion['cliente_id'],
            'user_id': asignacion['user_id'],
            'completado': False,
            'created_at': datetime.now()
        }

        return await cls.create(db, nueva_asignacion)
