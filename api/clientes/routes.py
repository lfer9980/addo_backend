from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from core.db import create_session
from core.utils.token import Manager
from app.usuarios.enums import UserTypeEnum
from app.usuarios.permissions import can_access

from app.clientes.schemas import *
from app.clientes.crud import ClienteCRUD

clientes_router = APIRouter()


@clientes_router.post('/create')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def create_cliente(cliente: CreateClienteSchema,
                         db: Session = Depends(create_session),
                         current_session: Depends = Depends(Manager),) -> ClienteSchema:

    CreateClienteSchema.model_validate(cliente)

    return await ClienteCRUD().create(db=db,
                                      cliente=cliente)


@clientes_router.put('/update/{rfc}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def update_cliente(rfc: str,
                         cliente: UpdateClienteSchema,
                         current_session: Depends = Depends(Manager),
                         db: Session = Depends(create_session)):

    UpdateClienteSchema.model_validate(cliente)  

    return await ClienteCRUD().update(
        db=db,
        cliente_update_rfc=rfc,
        cliente=cliente
    )



@clientes_router.delete('/delete/{rfc}')
@can_access(not_allowed=[UserTypeEnum.Colaborador])
async def delete_cliente(rfc: str,
                         current_session: Depends = Depends(Manager),
                         db: Session = Depends(create_session)):

    await ClienteCRUD().delete(db=db,
                               rfc=rfc)

    return {"message": f"Cliente con el RFC: {rfc} eliminado correctamente"}


@clientes_router.get('/get/all/{page}')
async def get_all_clientes(page: int,
                  db: Session = Depends(create_session),
                  current_session: Depends = Depends(Manager)) -> List[ClienteSchema]:

    return await ClienteCRUD().get_all(db=db,
                                       page=page,
                                       page_size=10)


@clientes_router.get('/get/{rfc}')
async def get_one_clientes(rfc: str,
                  db: Session = Depends(create_session),
                  current_session: Depends = Depends(Manager)) -> ClienteSchema:
    
    return await ClienteCRUD().get_one(db=db,
                                       rfc=rfc)
