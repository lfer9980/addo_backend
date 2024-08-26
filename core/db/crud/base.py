from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.orm import Session, Query


class BaseCRUD:

    @staticmethod
    async def _delete(db: Session, data) -> None:

        try:
            db.delete(data)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail=e,
            )

    @staticmethod
    async def _save(db: Session, data) -> None:
        try:
            db.add(data)
            db.commit()
            db.refresh(data)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail=e,
            )

    @staticmethod
    async def _update(db: Session, data) -> None:
        try:
            db.commit()
            db.refresh(data)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail=e,
            )

    @classmethod
    async def _exist(cls, db: Session, table, this_id: str) -> bool:

        data = db.query(table).where(
            getattr(table, 'id') == this_id
        )

        return True if data.first() is not None else False

    @staticmethod
    async def _filter_by(db: Session, table, key: str, data: str) -> Query:

        valid_keys = table.__mapper__.c.keys()
        if key not in valid_keys:
            raise HTTPException(
                status_code=404,
                detail=f"Key '{key}' not found in table '{table.table_name()}'"
            )

        data = db.query(table).where(
            getattr(table, key) == data
        )
        
        return data

    @classmethod
    async def _get_one(cls, db: Session, table, this_id: str):

        data: Query = await cls._filter_by(db=db,
                                           table=table,
                                           key='id',
                                           data=this_id)

        data = data.first()
        if data is None:
            raise HTTPException(status_code=404,
                                detail="Este id no esta registrado")

        return data

    @staticmethod
    async def _get_all(db: Session, table, page: int = 1, page_size: int = 10):

        offset = (page - 1) * page_size

        query = select(table).offset(offset).limit(page_size)
        result = db.execute(query)
        data = result.scalars().all()

        return data
    
    @staticmethod
    async def _get_by_relationship(cls, db: Session, table, key: str, data: str, page: int = 1, page_size: int = 10):

        data: Query = await cls._filter_by(db=db,
                                           table=table,
                                           key=key,
                                           data=data)

        data = data.first()
        if data is None:
            raise HTTPException(status_code=404,
                                detail="No existen registros")

        return data

    @staticmethod
    async def _get_all_by_id(db: Session, table, key: str, value: str, page: int = 1, page_size: int = 10):

        offset = (page - 1) * page_size
        
        valid_keys = table.__mapper__.c.keys()
        
        if key not in valid_keys:
            raise HTTPException(
                status_code=404,
                detail=f"Key '{key}' not found in table '{table.table_name()}'"
            )

        query = select(table).where(
            getattr(table, key) == value
        ).offset(offset).limit(page_size)
        
        result = db.execute(query)
        data = result.scalars().all()
        
        return data