from core.enums import StrEnum

class EstadoAsignacionEnum(StrEnum):
    Progreso = "En Progreso"
    Retraso = "Retrasada"
    Enviada = "Enviada"
    Pagada = "Pagada"