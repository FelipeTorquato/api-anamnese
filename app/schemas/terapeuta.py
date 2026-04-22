from pydantic import BaseModel, ConfigDict


class TerapeutaBase(BaseModel):
    especialidade: str
    carga_horaria_semanal: int = 40
    limite_atendimentos: int = 0


class TerapeutaCreate(TerapeutaBase):
    usuario_id: int


class TerapeutaResponse(TerapeutaBase):
    id: int
    usuario_id: int

    model_config = ConfigDict(from_attributes=True)
