from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Enum, Integer, ForeignKey, DateTime, Boolean)

from app.clientes.enums import *
from core.db import BaseTable


class ClienteModel(BaseTable):

    __tablename__ = 'clientes'
    
    razon_social = Column(String,
                    unique=True,
                    nullable=False
                    )
    
    rfc = Column(String,
                 unique=True,
                 nullable=False
                 )
    
    persona = Column(Enum(PersonaEnum),
                nullable=False
                )
 
    regimen = Column(String,
                     nullable=False
                     )   
    
    sector = Column(Enum(SectorEnum),
                    nullable=False
                    )
    
    empleados = Column(Integer,
                  nullable=False
                  )
    
    volumen = Column(Enum(VolumeEnum),
                     nullable=False
                     )   
    
    prioridad = Column(Enum(PrioridadEnum),
                    nullable=False
                    )
    
    valor = Column(Integer,
                nullable=False,
                default=1,
                )
    
    email = Column(String,
                   nullable=False)
    
    tamano = Column(Enum(TamanoEnum),
                   nullable=False)
    
    contacto = Column(String,
                   nullable=True)
    
    telefono = Column(String,
                   nullable=True)
    
    complejidad = Column(Integer,
                   nullable=False)
    
    """
    tareas = relationship("TareaModel",
                          back_populates="cliente",
                          ) 
    """





