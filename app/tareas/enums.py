from core.enums import StrEnum


class RecurrenciaEnum(StrEnum):
    Mensual = 'Mensual'
    Quincenal = 'Quincenal'
    Catorcenal = 'Catorcenal'
    Asimilados = 'Asimilados'
    Variable = 'Variable'
    

class DepartamentoEnum(StrEnum):
    Contabilidad = "Contabilidad"
    Variable = "RRHH"
    Gerencia = "Gerencia"
    
class TipoTareaEnum(StrEnum):
    Recurrente = "Recurrente"
    Variable = "Variable"
    Extraordinaria = 'Extraordinaria'