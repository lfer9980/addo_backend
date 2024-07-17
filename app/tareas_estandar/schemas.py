from pydantic import Field
from uuid import uuid4
from typing import Optional

from app.tareas.enums import *
from core.schemas import BaseSchema


class BaseTareaEstandarSchema(BaseSchema):
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
                    "tipo": TipoTareaEnum.Recurrente
                }
            ]
        }
    }


class TareaEstandarSchema(BaseTareaEstandarSchema):
    ...


class CreateTareaEstandarSchema(BaseTareaEstandarSchema):
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


class UpdateTareaEstandarSchema(BaseTareaEstandarSchema):
    tarea: Optional[str] = Field(None)
    descripcion: Optional[str] = Field(None)
    departamento: Optional[DepartamentoEnum] = Field(None)
    recurrencia: Optional[RecurrenciaEnum] = Field(None)
    complejidad: Optional[int] = Field(None)
    enviar: Optional[bool] = Field(None)
    pagar: Optional[bool] = Field(None)
    tipo: Optional[TipoTareaEnum] = Field(None)

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
