from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Enum, Boolean, SmallInteger, ForeignKey)

from app.tareas.enums import *
from core.db import BaseTable


class TareaModel(BaseTable):
    __tablename__ = 'tareas'

    tarea = Column(String,
                    nullable=False)

    descripcion = Column(String,
                         default='',)

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
    
    cliente_rfc = Column(String, ForeignKey("clientes.rfc"))
    
    cliente = relationship("ClienteModel", back_populates="tareas", uselist=False)
    
    asignacion = relationship("AsignacionModel", back_populates="tarea", uselist=False)