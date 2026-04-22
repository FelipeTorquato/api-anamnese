from enum import Enum


class StatusAgenda(str, Enum):
    AGENDADO = "AGENDADO"
    PRESENTE = "PRESENTE"
    FALTOU = "FALTOU"
    CANCELADO = "CANCELADO"


class StatusPaciente(str, Enum):
    ATIVO = "ATIVO"
    INATIVO = "INATIVO"


class TipoDocumento(str, Enum):
    RG = "RG"
    COMPROVANTE_RESIDENCIA = "COMPROVANTE_RESIDENCIA"
    LAUDO_MEDICO = "LAUDO_MEDICO"
    RECEITA_MEDICA = "RECEITA_MEDICA"
    ANAMNESE = "ANAMNESE"


class TipoUsuario(str, Enum):
    ADMIN = "ADMIN"
    GESTOR = "GESTOR"
    TERAPEUTA = "TERAPEUTA"
