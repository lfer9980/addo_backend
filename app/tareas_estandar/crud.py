from typing import List
from sqlalchemy.orm import Session, Query
from fastapi import HTTPException

from core.db import BaseCRUD
from app.tareas_estandar.schemas import *
from app.models.tareas_estandar import TareaEstandarModel


class TareaEstandarCRUD(BaseCRUD):

    @classmethod
    async def create(cls, db: Session, tarea: CreateTareaEstandarSchema) -> TareaEstandarSchema:

        tarea_data = tarea.model_dump()

        db_tarea = TareaEstandarModel(**tarea_data)

        await cls._save(db=db,
                        data=db_tarea)

        return TareaEstandarSchema.model_validate(db_tarea)

    @classmethod
    async def update(cls, db: Session,
                     tarea_id: str,
                     tarea: UpdateTareaEstandarSchema) -> TareaEstandarSchema:

        old_tarea: Query = await cls._filter_by(db=db,
                                                table=TareaEstandarModel,
                                                key='id',
                                                data=tarea_id)

        old_tarea: TareaEstandarModel | None = old_tarea.first()
        if old_tarea is None:
            raise HTTPException(
                status_code=404,
                detail=f"Tarea estandar update failed: {tarea_id}"
            )

        new_tarea = tarea.model_dump()
        for key, value in new_tarea.items():
            if value is not None:
                setattr(old_tarea, key, value)

        await cls._update(db=db,
                          data=old_tarea)

        return TareaEstandarSchema.model_validate(old_tarea)

    @classmethod
    async def delete(cls, db: Session, tarea_id: str) -> None:

        tarea: Query = await cls._filter_by(db=db,
                                            table=TareaEstandarModel,
                                            key='id',
                                            data=tarea_id)
        tarea = tarea.first()

        if tarea is None:
            raise HTTPException(
                status_code=404,
                detail=f"Tarea estandar not found: {tarea_id}"
            )

        await cls._delete(db=db,
                          data=tarea)

    @classmethod
    async def get_all(cls, db: Session, page: int = 1, page_size: int = 10) -> List[TareaEstandarSchema]:

        tareas_estandar = await cls._get_all(db=db,
                                            table=TareaEstandarModel,
                                            page=page, 
                                            page_size=page_size)

        return [TareaEstandarSchema.model_validate(tarea) for tarea in tareas_estandar]

    @classmethod
    async def get_one(cls, db: Session, tarea_id: str) -> TareaEstandarSchema:

        tarea_estandar = await cls._get_one(db=db,
                                            table=TareaEstandarModel,
                                            this_id=tarea_id)

        return TareaEstandarSchema.model_validate(tarea_estandar)
