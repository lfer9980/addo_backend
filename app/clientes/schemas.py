import re
from pydantic import EmailStr, model_validator, field_validator

from core.str import RFC_REGEX
from app.clientes.enums import *
from core.schemas import BaseSchema


class BaseClienteSchema(BaseSchema):
    razon_social: str
    rfc: str
    persona: PersonaEnum
    regimen: str
    sector: SectorEnum
    empleados: int
    volumen: VolumeEnum
    prioridad: PrioridadEnum
    valor: int
    email: EmailStr
    contacto: str
    telefono: str
    tamano: TamanoEnum
    complejidad: int

    @staticmethod
    def _valid_rfc(rfc: str) -> bool:
        rfc = rfc.upper()
        return True if re.match(RFC_REGEX, rfc) else False

    @field_validator('rfc')
    @classmethod
    def validate(cls, rfc: str) -> str:
        rfc_valid: bool = cls._valid_rfc(rfc)
        if not rfc_valid:
            raise ValueError("RFC is invalid")

        return rfc.upper()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "razon_social": "example@example.com",
                    "rfc": "FEAL980607LSA",
                    "persona": "Persona Moral",
                    "regimen": "Regimen 1",
                    "sector": "industria",
                    "empleados": 50,
                    "volumen": 4,
                    "prioridad": 8,
                    "valor": 2,
                    "email": "mail@mail.com",
                    "contacto": "Angel fernandez",
                    "telefono": "+526141751832",
                    "tamano": 3,
                    "complejidad": 3,
                }
            ]
        }
    }


class ClienteSchema(BaseClienteSchema):
    ...

class ClienteById(BaseSchema):
    razon_social: str
    rfc: str

class CreateClienteSchema(BaseClienteSchema):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                   "razon_social": "example@example.com",
                    "rfc": "FEAL980607LSA",
                    "persona": "Persona Moral",
                    "regimen": "Regimen 1",
                    "sector": "industria",
                    "empleados": 50,
                    "volumen": 4,
                    "prioridad": 8,
                    "valor": 2,
                    "email": "mail@mail.com",
                    "contacto": "Angel fernandez",
                    "telefono": "+526141751832",
                    "tamano": 3,
                    "complejidad": 3,
                }
            ]
        }
    }


class UpdateClienteSchema(BaseClienteSchema):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                   "razon_social": "example@example2.com",
                    "rfc": "BSE231016AP0",
                    "persona": "Persona Moral",
                    "regimen": "Regimen 1",
                    "sector": "industria",
                    "empleados": 50,
                    "volumen": 4,
                    "prioridad": 8,
                    "valor": 2,
                    "email": "mail@mail2.com",
                    "contacto": "Angel fernandez",
                    "telefono": "+526141751832",
                    "tamano": 3,
                    "complejidad": 3,
                }
            ]
        }
    }
