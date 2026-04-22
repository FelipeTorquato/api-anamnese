from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class EvolucaoBase(BaseModel):
    descricao: str = Field(..., min_length=10)


class EvolucaoCreate(EvolucaoBase):
    pass


class EvolucaoResponse(EvolucaoBase):
    id: int
    atendimento_id: int
    inativo: bool
    created_at: datetime
    created_by: str

    model_config = ConfigDict(from_attributes=True)


class AtendimentoCreate(BaseModel):
    agenda_id: int


class AtendimentoResponse(BaseModel):
    id: int
    agenda_id: int
    evolucao: Optional[EvolucaoResponse] = None

    model_config = ConfigDict(from_attributes=True)
