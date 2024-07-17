from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Enum, Boolean, SmallInteger, ForeignKey)

from app.tareas.enums import *
from core.db import BaseTable


class TareaModel(BaseTable):
    __tablename__ = 'tareas'

    cliente_id = Column(String,
                        ForeignKey("clientes.id"))

    tarea = Column(String,
                    nullable=False)

    descripcion = Column(String,
                         default='',
                         nullable=False)

    departamento = Column(Enum(DepartamentoEnum),
                       default='Categoria no asignada',
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
                  nullable=False)
