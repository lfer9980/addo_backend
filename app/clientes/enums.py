from core.enums import StrEnum, NumEnum


class PersonaEnum(StrEnum):
    PersonaFisica = 'Persona Fisica'
    PersonaMoral = 'Persona Moral'


class SectorEnum(StrEnum):
    Industria = 'industria'
    Comercio = 'comercio'
    Servicios = 'servicios'


class TamanoEnum(NumEnum):
    Micro = 1
    Peque = 2
    Mediana = 3
    Gran = 4


class VolumeEnum(NumEnum):
    A = 1
    B = 2
    C = 3
    D = 4


class PrioridadEnum(NumEnum):
    A = 10
    B = 8
    C = 5
    D = 3
    E = 2
    F = 1
