from typing import List
from sqlalchemy.orm import Session, Query
from fastapi import HTTPException

from core.db import BaseCRUD
from app.tareas_estandar.schemas import *
from app.models.tareas_estandar import TareaEstandarModel


class TareaEstandarCRUD(BaseCRUD):
    
    current_table = TareaEstandarModel

    @classmethod
    async def create(cls, db: Session, tarea: CreateTareaEstandarSchema) -> TareaEstandarSchema:

        tarea_data = tarea.model_dump()

        db_tarea = cls.current_table(**tarea_data)

        await cls._save(db=db,
                        data=db_tarea)

        return TareaEstandarSchema.model_validate(db_tarea)

    @classmethod
    async def update(cls, db: Session,
                     tarea_id: str,
                     tarea: UpdateTareaEstandarSchema) -> TareaEstandarSchema:

        old_tarea: Query = await cls._get_one(db=db,
                                              table=cls.current_table,
                                              this_id=tarea_id,
                                              )
        if old_tarea is None:
            raise HTTPException(
                status_code=404,
                detail=f"Tarea estandar no encontrada: {tarea_id}"
            )

        new_tarea = tarea.model_dump()
        
        for key, value in new_tarea.items():
            if value is not None:
                setattr(old_tarea, key, value)

        await cls._update(db=db, data=old_tarea)

        return TareaEstandarSchema.model_validate(old_tarea)

    @classmethod
    async def delete(cls, db: Session, tarea_id: str) -> None:

        tarea: Query = await cls._filter_by(db=db,
                                            table=cls.current_table,
                                            key='id',
                                            data=tarea_id)
        tarea = tarea.first()

        if tarea is None:
            raise HTTPException(
                status_code=404,
                detail=f"Tarea estandar no encontrada: {tarea_id}"
            )

        await cls._delete(db=db,
                          data=tarea)

    @classmethod
    async def get_all(cls, db: Session, 
                      page: int = 1, 
                      page_size: int = 10) -> List[TareaEstandarSchema]:

        tareas_estandar = await cls._get_all(db=db,
                                            table=cls.current_table,
                                            page=page, 
                                            page_size=page_size)

        return [TareaEstandarSchema.model_validate(tarea) for tarea in tareas_estandar]

    @classmethod
    async def get_one(cls, db: Session, tarea_id: str) -> TareaEstandarSchema:

        tarea_estandar = await cls._get_one(db=db,
                                            table=cls.current_table,
                                            this_id=tarea_id)

        return TareaEstandarSchema.model_validate(tarea_estandar)
