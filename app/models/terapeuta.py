from typing import List, TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.models import Usuario, Paciente, Agenda
from app.models.base import Base, AuditMixin
from .associations import paciente_terapeuta_table

if TYPE_CHECKING:
    from .usuario import Usuario
    from .paciente import Paciente
    from .agenda import Agenda


class Terapeuta(Base, AuditMixin):
    __tablename__ = "terapeutas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    especialidade: Mapped[str] = mapped_column(String(100))
    carga_horaria_semanal: Mapped[int] = mapped_column(default=40)
    limite_atendimentos: Mapped[int] = mapped_column(default=0)

    usuario: Mapped["Usuario"] = relationship(back_populates="terapeuta")
    pacientes: Mapped[List["Paciente"]] = relationship(
        secondary=paciente_terapeuta_table, back_populates="terapeutas"
    )
    agendamentos: Mapped[List["Agenda"]] = relationship(back_populates="terapeuta")
