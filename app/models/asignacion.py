from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, ForeignKey, Boolean, DateTime)

from core.db import BaseTable


class AsignacionModel(BaseTable):
    __tablename__ = 'asignaciones'

    tarea_id = Column(String,
                      ForeignKey("tareas.id"),
                      primary_key=True,)

    usuario_id = Column(String,
                        ForeignKey("usuarios.id"),
                        primary_key=True)

    created_at = Column(DateTime,
                        default=datetime.utcnow())

    finished_at = Column(DateTime)

    completado = Column(Boolean,
                        default=False)
