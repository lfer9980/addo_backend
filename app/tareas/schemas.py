import pytz
from datetime import datetime

from pydantic import Field
from uuid import uuid4, UUID
from typing import Optional
from datetime import datetime, timezone

from app.tareas.enums import *
from app.asignaciones.enums import *
from core.schemas import BaseSchema
from app.asignaciones.enums import *

class BaseTareaSchema(BaseSchema):
    id: str = Field(default_factory=lambda: str(uuid4()))
    tarea: str
    descripcion: str
    departamento: DepartamentoEnum
    recurrencia: RecurrenciaEnum
    complejidad: int
    enviar: bool
    pagar: bool
    tipo: TipoTareaEnum
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tarea": "Nombre tarea",
                    "descripcion": "Ejemplo de tarea",
                    "departamento": DepartamentoEnum.Contabilidad,
                    "recurrencia": RecurrenciaEnum.Mensual,
                    "complejidad": 1,
                    "enviar": True,
                    "pagar": False,
                    "tipo": TipoTareaEnum.Recurrente,
                    "username": "default",
                }
            ]
        }
    }


class TareaSchema(BaseTareaSchema):
    cliente_rfc: str

class CreateTareaSchema(BaseTareaSchema):
    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str

class TareaGetUserSchema(BaseTareaSchema):
    cliente_rfc: str 
    razon_social: str
    estado: EstadoAsignacionEnum
    completado: bool
    creado: datetime
    
class TareaGetClientSchema(BaseTareaSchema):
    username: Optional[str] = Field(None)
    estado: EstadoAsignacionEnum
    completado: bool
    creado: datetime
    
class TareaGetAllSchema(BaseTareaSchema):
    cliente_rfc: str 
    razon_social: str
    username: Optional[str] = Field(None)
    estado: EstadoAsignacionEnum
    completado: bool
    creado: datetime
    
class UpdateTareaSchema(BaseSchema):
    tarea: str
    descripcion: str
    departamento: DepartamentoEnum
    recurrencia: RecurrenciaEnum
    complejidad: int
    enviar: bool
    pagar: bool
    tipo: TipoTareaEnum
    username: str
    
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tarea": "Nombre tarea",
                    "descripcion": "Ejemplo de tarea",
                    "departamento": DepartamentoEnum.Contabilidad,
                    "recurrencia": RecurrenciaEnum.Mensual,
                    "complejidad": 1,
                    "enviar": True,
                    "pagar": False,
                    "tipo": TipoTareaEnum.Recurrente,
                    "username": "default"
                }
            ]
        }
    }
    

class TareaResponse(BaseTareaSchema):
    username: str
    completado: bool
    estado: EstadoAsignacionEnum
    creado: datetime
    ultimo_cambio: datetime
