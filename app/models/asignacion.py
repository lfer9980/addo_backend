from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, ForeignKey, Enum, Boolean, DateTime)

from core.db import BaseTable
from app.asignaciones.enums import *


class AsignacionModel(BaseTable):
    __tablename__ = 'asignaciones'

    estado = Column(Enum(EstadoAsignacionEnum),
                        default=EstadoAsignacionEnum.Progreso)
   
    completado = Column(Boolean,
                        default=False)
    
    creado = Column(DateTime,
                    default=datetime.now())
    
    ultimo_cambio = Column(DateTime,
                           default=datetime.now())

    terminado = Column(DateTime)
    
    tarea = relationship("TareaModel", back_populates="asignacion")
    
    usuario = relationship("UsuarioModel", back_populates="asignaciones", uselist=False)