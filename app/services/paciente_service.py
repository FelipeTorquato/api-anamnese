from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Paciente
from app.repositories.paciente_repository import PacienteRepository
from app.repositories.responsavel_repository import ResponsavelRepository
from app.schemas.paciente import PacienteCreate


def criar_paciente(db: Session, paciente_in: PacienteCreate) -> Paciente:
    paciente_existente = PacienteRepository.buscar_por_rg(db, paciente_in.rg)
    if paciente_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Já existe um paciente com este RG cadastrado.")

    responsaveis_db = ResponsavelRepository.buscar_por_ids(db, paciente_in.responsaveis_ids)

    if not responsaveis_db or len(responsaveis_db) != len(paciente_in.responsaveis_ids):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Um ou mais responsáveis não foram encontrados no sistema.")

    dados_paciente = paciente_in.model_dump(exclude={"responsaveis_ids"})

    novo_paciente = Paciente(**dados_paciente)

    novo_paciente.responsaveis = responsaveis_db

    return PacienteRepository.criar(db, novo_paciente)


def listar_pacientes(db: Session, skip: int = 0, limit: int = 100) -> List[Paciente]:
    return PacienteRepository.listar(db, skip, limit)
