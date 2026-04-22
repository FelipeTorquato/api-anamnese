from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.models import Agenda
from app.models.base import Base, AuditMixin

if TYPE_CHECKING:
    from .agenda import Agenda


class Atendimento(Base, AuditMixin):
    __tablename__ = "atendimentos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    agenda_id: Mapped[int] = mapped_column(ForeignKey("agendas.id"), unique=True)

    agenda: Mapped["Agenda"] = relationship(back_populates="atendimento")
    evolucao: Mapped[Optional["Evolucao"]] = relationship(back_populates="atendimento")


class Evolucao(Base, AuditMixin):
    __tablename__ = "evolucoes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    atendimento_id: Mapped[int] = mapped_column(ForeignKey("atendimentos.id"), unique=True)
    descricao: Mapped[str] = mapped_column(Text)
    inativo: Mapped[bool] = mapped_column(default=False)

    atendimento: Mapped["Atendimento"] = relationship(back_populates="evolucao")
