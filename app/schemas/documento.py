from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models import TipoDocumento


class DocumentoResponse(BaseModel):
    id: int
    paciente_id: int
    tipo: TipoDocumento
    caminho_arquivo: str
    observacao: Optional[str] = None
    created_at: datetime
    created_by: str

    model_config = ConfigDict(from_attributes=True)
