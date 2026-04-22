from sqlalchemy import Table, Column, ForeignKey
from .base import Base

paciente_responsavel_table = Table(
    "paciente_responsavel",
    Base.metadata,
    Column("paciente_id", ForeignKey("pacientes.id"), primary_key=True),
    Column("responsavel_id", ForeignKey("responsaveis.id"), primary_key=True),
)

paciente_terapeuta_table = Table(
    "paciente_terapeuta",
    Base.metadata,
    Column("paciente_id", ForeignKey("pacientes.id"), primary_key=True),
    Column("terapeuta_id", ForeignKey("terapeutas.id"), primary_key=True),
)
