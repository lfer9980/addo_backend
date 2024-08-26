from typing import List, Tuple
from fastapi import HTTPException
from sqlalchemy.orm import Session, Query

from core.db import BaseCRUD
from app.clientes.schemas import *
from app.models.clientes import ClienteModel


class ClienteCRUD(BaseCRUD):
    current_table = ClienteModel

    @classmethod
    async def _validate_unique(cls, db: Session, cliente) -> None:

        fields_to_check: Tuple = (
            ("email", cliente.email),
            ("rfc", cliente.rfc),
            ("razon_social", cliente.razon_social)
        )

        for field, value in fields_to_check:
            exists = await cls._filter_by(db=db,
                                          table=ClienteModel,
                                          key=field,
                                          data=value)
            if exists.first():
                raise HTTPException(
                    status_code=400,
                    detail=f"{field.replace('_', ' ').capitalize()} exists already.",
                )

    @classmethod
    async def create(cls, db: Session, cliente: CreateClienteSchema) -> ClienteSchema:

        await cls._validate_unique(db, cliente)
        
        cliente_data = cliente.model_dump()
        db_cliente = ClienteModel(**cliente_data)

        await cls._save(db, db_cliente)

        return ClienteSchema.model_validate(db_cliente)

    @classmethod
    async def update(cls, db: Session, cliente_update_rfc: str, cliente: UpdateClienteSchema) -> ClienteSchema:
        
        old_cliente: Query = await cls._filter_by(db=db,
                                                  table=ClienteModel,
                                                  key='rfc',
                                                  data=cliente_update_rfc)

        old_cliente: ClienteModel | None = old_cliente.first()

        if old_cliente is None:
            raise HTTPException(status_code=404,
                                detail="Client not found")

        new_user = cliente.model_dump()

        for key, value in new_user.items():
            if value is not None:
                setattr(old_cliente, key, value)

        await cls._update(db, old_cliente)

        return ClienteSchema.model_validate(old_cliente)

    @classmethod
    async def delete(cls, db: Session, rfc: str) -> None:

        cliente: Query = await cls._filter_by(db=db,
                                              table=ClienteModel,
                                              key='rfc',
                                              data=rfc)
        cliente: ClienteModel | None = cliente.first()
        
        if cliente is None:
            raise HTTPException(
                status_code=400,
                detail='Cliente no encontrado'
            )

        await cls._delete(db, cliente)

    @classmethod
    async def get_all(cls, db: Session, page: int = 1, page_size: int = 10) -> List[ClienteSchema]:

        clientes = await cls._get_all(db=db,
                                      page=page,
                                      page_size=page_size,
                                      table=ClienteModel, )

        return [ClienteSchema.model_validate(cliente) for cliente in clientes]

    @classmethod
    async def get_one(cls, db: Session, rfc: str) -> ClienteSchema:
        cliente: Query = await cls._filter_by(db=db,
                                              table=ClienteModel,
                                              key='rfc',
                                              data=rfc)
        cliente = cliente.first()

        if cliente is None:
            raise HTTPException(
                status_code=400,
                detail='Cliente no encontrado'
            )

        return ClienteSchema.model_validate(cliente)
    
    @classmethod
    async def get_one_by_id(cls, db: Session, cliente_id: str) -> ClienteById:
        
        cliente = await cls._get_one(db=db, 
                               table=cls.current_table,
                               this_id=cliente_id)

        if cliente is None:
            raise HTTPException(
                status_code=400,
                detail='Cliente no encontrado'
            )

        return ClienteById.model_validate(cliente)
