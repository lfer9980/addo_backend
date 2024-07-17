from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Enum, Boolean, SmallInteger, ForeignKey)

from app.tareas.enums import *
from core.db import BaseTable


class TareaEstandarModel(BaseTable):
    __tablename__ = 'tareas_estandar'

    tarea = Column(String,
                    nullable=False)

    descripcion = Column(String,
                         nullable=False)

    departamento = Column(Enum(DepartamentoEnum),
                       nullable=False)

    recurrencia = Column(Enum(RecurrenciaEnum),
                         nullable=False)

    complejidad = Column(SmallInteger,
                         nullable=False,
                         default=1,
                         )

    enviar = Column(Boolean,
                      default=False,
                      nullable=False)

    pagar = Column(Boolean,
                           default=False,
                           nullable=False)

    tipo = Column(Enum(TipoTareaEnum),
                  default=False,
                  nullable=False)
