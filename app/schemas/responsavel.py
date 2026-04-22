from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ResponsavelBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150)
    cpf: str = Field(..., min_length=11, max_length=11, description="Apenas números")
    telefone: str = Field(..., min_length=8, max_length=20)


class ResponsavelCreate(ResponsavelBase):
    pass


class ResponsavelUpdate(BaseModel):
    nome: Optional[str] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None


class ResponsavelResponse(ResponsavelBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
