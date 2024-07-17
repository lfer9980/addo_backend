from datetime import datetime

from core.schemas import BaseSchema


class AsignacionBase(BaseSchema):
    tarea_id: str
    usuario_id: str
    completado: bool = False
    created_at: datetime = datetime.now()


class AsignacionCreate(AsignacionBase):
    tarea_id: str
    usuario_id: str
    completado: bool = False
    created_at: datetime = datetime.now()


class AsignacionUpdate(AsignacionBase):
    id_usuario: str


class AsignacionDelete(AsignacionBase):
    ...


class AsignacionResponse(BaseSchema):
    username: str
    tarea_id: str
    completado: bool
    created_at: datetime = datetime.now()
