from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.models import Atendimento
from app.models.base import Base, AuditMixin
from .enums import StatusAgenda

if TYPE_CHECKING:
    from .paciente import Paciente
    from .terapeuta import Terapeuta
    from .prontuario import Atendimento


class Agenda(Base, AuditMixin):
    __tablename__ = "agendas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"))
    terapeuta_id: Mapped[int] = mapped_column(ForeignKey("terapeutas.id"))
    data_hora_inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    data_hora_fim: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    status: Mapped[StatusAgenda] = mapped_column(Enum(StatusAgenda), default=StatusAgenda.AGENDADO)
    motivo_cancelamento: Mapped[Optional[str]] = mapped_column(Text)
    agendamento_original_id: Mapped[Optional[int]] = mapped_column(ForeignKey("agendas.id"))

    paciente: Mapped["Paciente"] = relationship(back_populates="agendamentos")
    terapeuta: Mapped["Terapeuta"] = relationship(back_populates="agendamentos")
    atendimento: Mapped[Optional["Atendimento"]] = relationship(back_populates="agenda")
