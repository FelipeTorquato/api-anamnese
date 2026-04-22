from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.enums import StatusAgenda


class AgendaBase(BaseModel):
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: StatusAgenda = StatusAgenda.AGENDADO


class AgendaCreate(AgendaBase):
    paciente_id: int
    terapeuta_id: int

    @model_validator(mode='after')
    def validar_horarios(self) -> 'AgendaCreate':
        if self.data_hora_fim <= self.data_hora_inicio:
            raise ValueError("O horário de fim deve ser posterior ao horário de início.")
        return self


class AgendaResponse(AgendaBase):
    id: int
    paciente_id: int
    terapeuta_id: int
    motivo_cancelamento: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
