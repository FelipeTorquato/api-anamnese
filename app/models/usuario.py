from typing import Optional, TYPE_CHECKING

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.models import Terapeuta
from app.models.base import Base, AuditMixin
from .enums import TipoUsuario

if TYPE_CHECKING:
    from .terapeuta import Terapeuta

class Usuario(Base, AuditMixin):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    perfil: Mapped[TipoUsuario] = mapped_column(Enum(TipoUsuario))

    terapeuta: Mapped[Optional["Terapeuta"]] = relationship(back_populates="usuario")
