from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.models import Paciente
from app.models.base import Base, AuditMixin
from .associations import paciente_responsavel_table

if TYPE_CHECKING:
    from .paciente import Paciente


class Responsavel(Base, AuditMixin):
    __tablename__ = "responsaveis"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(150))
    cpf: Mapped[str] = mapped_column(String(11), unique=True)
    telefone: Mapped[str] = mapped_column(String(20))

    pacientes: Mapped[List["Paciente"]] = relationship(
        secondary=paciente_responsavel_table, back_populates="responsaveis"
    )
