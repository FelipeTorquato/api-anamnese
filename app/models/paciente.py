from datetime import datetime
from typing import List, TYPE_CHECKING

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.associations import paciente_responsavel_table, paciente_terapeuta_table
from app.models.base import Base, AuditMixin
from .enums import StatusPaciente

if TYPE_CHECKING:
    from .responsavel import Responsavel
    from .terapeuta import Terapeuta
    from .documento import Documento
    from .agenda import Agenda


class Paciente(Base, AuditMixin):
    __tablename__ = "pacientes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(150), index=True)
    data_nascimento: Mapped[datetime] = mapped_column(DateTime)
    rg: Mapped[str] = mapped_column(String(20))
    status: Mapped[StatusPaciente] = mapped_column(Enum(StatusPaciente), default=StatusPaciente.ATIVO)

    responsaveis: Mapped[List["Responsavel"]] = relationship(
        secondary=paciente_responsavel_table, back_populates="pacientes"
    )
    terapeutas: Mapped[List["Terapeuta"]] = relationship(
        secondary=paciente_terapeuta_table, back_populates="pacientes"
    )
    documentos: Mapped[List["Documento"]] = relationship(back_populates="paciente")
    agendamentos: Mapped[List["Agenda"]] = relationship(back_populates="paciente")
