import sys
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Enum, DateTime)

from app.usuarios.enums import *
from core.db import BaseTable


class UsuarioModel(BaseTable):
    __tablename__ = 'usuarios'

    username = Column(String,
                      unique=True,
                      nullable=False,
                      )

    password = Column(String,
                      nullable=False)

    posicion = Column(String,
                      nullable=True)

    user_type = Column(Enum(UserTypeEnum),
                       default=UserTypeEnum.Colaborador,
                       )

    avatar = Column(String,
                    unique=False,
                    nullable=False,
                    default='',
                    )

    created_at = Column(DateTime,
                        default=datetime.datetime.now(datetime.timezone.utc),
                        )

    """     
    asignaciones = relationship("AsignacionModel",
                                back_populates="colaborador")

    puntaje = relationship("PuntajeModel",
                           back_populates="colaborador")
    """