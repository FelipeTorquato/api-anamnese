from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import StatusPaciente
from app.schemas.terapeuta import TerapeutaResponse


class PacienteBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150)
    data_nascimento: datetime
    rg: str
    status: StatusPaciente = StatusPaciente.ATIVO


class PacienteCreate(PacienteBase):
    responsaveis_ids: List[int] = Field(..., min_length=1)


class PacienteUpdate(BaseModel):
    nome: Optional[str] = None
    status: Optional[StatusPaciente] = None


class PacienteResponse(PacienteBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PacienteDetalhadoResponse(PacienteResponse):

    terapeutas: List[TerapeutaResponse] = []
    # responsaveis: List[ResponsavelResponse] = []