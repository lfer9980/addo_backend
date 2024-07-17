from datetime import datetime

from pydantic import Field
from uuid import uuid4, UUID
from typing import Optional

from app.tareas.enums import *
from core.schemas import BaseSchema


class BaseTareaSchema(BaseSchema):
    id: str = Field(default_factory=lambda: str(uuid4()))
    tarea: str
    descripcion: str
    departamento: DepartamentoEnum
    recurrencia: RecurrenciaEnum
    complejidad: int
    enviar: bool = True
    pagar: bool = False
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
                    "tipo": TipoTareaEnum.Recurrente
                }
            ]
        }
    }


class TareaSchema(BaseTareaSchema):
    ...

class CreateTareaSchema(BaseTareaSchema):
    id: str = Field(default_factory=lambda: str(uuid4()))
    usuario_id: str


class UpdateTareaSchema(BaseSchema):
    tarea: str
    recurrencia: RecurrenciaEnum
    usuario_id: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tarea": "Nombre tarea",
                    "recurrencia": RecurrenciaEnum.Mensual,
                    "usuario_id": "id de usuario",
                }
            ]
        }
    }
    



class TareaResponse(BaseTareaSchema):
    username: str
    completado: bool
    created_at: datetime = datetime.now()
