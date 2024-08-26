import sys
import pytz
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Integer, ForeignKey, DateTime)

from core.db import BaseTable


class PuntajeModel(BaseTable):
    __tablename__ = 'puntajes'

    puntaje = Column(Integer,
                     nullable=False,
                     default=0
                     )

    fecha_actualizacion = Column(DateTime,
                                 default=datetime.now(pytz.timezone('Etc/GMT+6')))
    
    username = Column(String,
                        ForeignKey("usuarios.username")
                        )
    
    usuario = relationship("UsuarioModel", back_populates=False, uselist=False)
