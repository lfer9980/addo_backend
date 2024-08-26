import pytz
from datetime import datetime

from core.schemas import BaseSchema
from app.asignaciones.enums import *

class AsignacionBase(BaseSchema):
    tarea_id: str
    username: str
    estado: EstadoAsignacionEnum
    completado: bool = False
    creado: datetime = datetime.now(pytz.timezone('Etc/GMT+6'))
    ultimo_cambio: datetime = datetime.now(pytz.timezone('Etc/GMT+6'))

class AsignacionCreate(AsignacionBase):
    tarea_id: str
    username: str
    estado: EstadoAsignacionEnum
    completado: bool = False
    creado: datetime = datetime.now(pytz.timezone('Etc/GMT+6'))


class AsignacionUpdate(AsignacionBase):
    tarea_id: str
    username: str


class AsignacionDelete(AsignacionBase):
    ...

class AsignacionResponse(BaseSchema):
    username: str
    tarea_id: str
    estado: EstadoAsignacionEnum
    completado: bool
    creado: datetime = datetime.now(pytz.timezone('Etc/GMT+6'))
    ultimo_cambio: datetime
