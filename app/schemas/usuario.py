from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.models import TipoUsuario


class UsuarioBase(BaseModel):
    email: EmailStr
    perfil: TipoUsuario


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8, max_length=50)


class UsuarioResponse(UsuarioBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
