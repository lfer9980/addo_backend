import re
from uuid import uuid4
from typing import Optional
from pydantic import model_validator, Field

from core.str import *
from core.schemas import BaseSchema
from app.usuarios.enums import *


class BaseUserSchema(BaseSchema):
    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str
    nombres: str
    apellidos: str
    posicion: str
    tipo_usuario: UserTypeEnum

    @classmethod
    def validate_password(cls, password: str) -> None:
        return re.match(PASSWORD_REGEX, password)


class UserSchema(BaseUserSchema):
    username: str
    nombres: str
    apellidos: str
    posicion: str
    tipo_usuario: UserTypeEnum
    avatar: str


class LoginUserSchema(BaseUserSchema):
    password: str


class UpdateOwnUserSchema(BaseSchema):
    old_password: Optional[str] = Field(None)
    new_password: Optional[str] = Field(None)
    confirm_new_password: Optional[str] = Field(None)

    @classmethod
    def _valid_password(cls, password: str) -> None:
        return re.match(PASSWORD_REGEX, password)

    @classmethod
    @model_validator(mode='before')
    def validate(cls, data: dict) -> dict:

        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password is None:
            return data

        if confirm_new_password is None and new_password:
            raise ValueError('New password and confirm new password are required')

        if data['new_password'] != data['confirm_new_password']:
            raise ValueError('Password and confirmation do not match')

        if not cls._valid_password(data['new_password']):
            raise ValueError('Password does not match to pattern')

        return data

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "old_password": "Sf23s2g4.",
                    "new_password": "Sf23s2g4.2",
                    "confirm_new_password": "Sf23s2g4.2",
                }
            ]
        }
    }


class UpdateUserSchema(BaseSchema):
    username: str
    nombres: str
    apellidos: str
    posicion: str
    avatar: str
    tipo_usuario: Optional[UserTypeEnum] = Field(None)
    new_password: Optional[str] = Field(None)
    confirm_new_password: Optional[str] = Field(None)

    @classmethod
    def _valid_password(cls, password: str) -> None:
        return re.match(PASSWORD_REGEX, password)

    @model_validator(mode='before')
    @classmethod
    def validate(cls, data: dict) -> dict:
        new_password = data.get('new_password')

        if new_password is None:
            return data

        if not cls._valid_password(data['new_password']):
            raise ValueError('Password does not match to pattern')

        return data

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "angelFernandez",
                    "nombres": "Angel",
                    "apellidos": "Fernandez",
                    'posicion': 'Auxiliar contable',
                    "avatar": "",
                    'tipo_usuario': UserTypeEnum.Colaborador,
                    'new_password': 'Fo12345$',
                    'confirm_new_password': 'Fo12345$',
                }
            ]
        }
    }


class CreateUserSchema(BaseUserSchema):
    username: str
    nombres: str
    apellidos: str
    posicion: str
    tipo_usuario: UserTypeEnum
    avatar: str = ''
    password: str
    confirm_password: str = Field(...)

    @classmethod
    @model_validator(mode='before')
    def validate(cls, data: dict) -> dict:
        if data['password'] != data['confirm_password']:
            raise ValueError('Password and confirmation do not match')

        if not cls.validate_password(data['password']):
            raise ValueError('Password does not match to pattern')

        if data["tipo_usuario"] == UserTypeEnum.SupeAdmin:
            raise ValueError("User type could not be Admin")

        return data

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "angelFernandez",
                    "nombres": "Angel",
                    "apellidos": "Fernandez",
                    'posicion': 'Auxiliar contable',
                    'tipo_usuario': UserTypeEnum.Colaborador,
                    "avatar": "",
                    'password': 'Fo12345',
                    'confirm_password': 'Fo12345',
                }
            ]
        }
    }
