from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, AuditMixin
from .enums import TipoDocumento

if TYPE_CHECKING:
    from .paciente import Paciente


class Documento(Base, AuditMixin):
    __tablename__ = "documentos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    tipo: Mapped[TipoDocumento] = mapped_column(Enum(TipoDocumento))
    caminho_arquivo: Mapped[str] = mapped_column(String(500))
    observacao: Mapped[Optional[str]] = mapped_column(Text)

    paciente: Mapped["Paciente"] = relationship(back_populates="documentos")
