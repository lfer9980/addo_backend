import pytz
import sys
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Enum, DateTime, ForeignKey)

from app.usuarios.enums import *
from core.db import BaseTable


class UsuarioModel(BaseTable):
    __tablename__ = 'usuarios'

    username = Column(String,
                      unique=True,
                      nullable=False,
                      )
    
    nombres = Column(String,
                      nullable=False)
    
    apellidos = Column(String,
                      nullable=False)

    posicion = Column(String,
                      nullable=True)

    tipo_usuario = Column(Enum(UserTypeEnum),
                          default=UserTypeEnum.Colaborador,
                          )

    avatar = Column(String,
                    unique=False,
                    nullable=False,
                    default='',
                    )

    password = Column(String,
                      nullable=False)
    
    creado = Column(DateTime,
                    default=datetime.now(pytz.timezone('Etc/GMT+6')),
                        )

    asignacion_id = Column(String, ForeignKey("asignaciones.id"))

    asignaciones = relationship("AsignacionModel", back_populates="usuario")

    puntaje = relationship("PuntajeModel", back_populates="usuario")