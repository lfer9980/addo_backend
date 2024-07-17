import sys
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Integer, ForeignKey, DateTime)

from core.db import BaseTable


class PuntajeModel(BaseTable):
    __tablename__ = 'puntajes'

    usuario_id = Column(String,
                        ForeignKey("usuarios.id"),
                        )

    puntaje = Column(Integer,
                     nullable=False,
                     default=0
                     )

    fecha_actualizacion = Column(DateTime,
                                 default=datetime.datetime.now(datetime.timezone.utc))
