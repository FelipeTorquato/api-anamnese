from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Responsavel
from app.repositories.responsavel_repository import ResponsavelRepository
from app.schemas.responsavel import ResponsavelCreate, ResponsavelUpdate


def criar_responsavel(db: Session, responsavel_in: ResponsavelCreate) -> Responsavel:
    responsavel_existente = ResponsavelRepository.buscar_por_cpf(db, responsavel_in.cpf)
    if responsavel_existente:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Responsável com CPF já cadastrado")

    novo_responsavel = Responsavel(**responsavel_in.model_dump())
    return ResponsavelRepository.criar(db, novo_responsavel)


def buscar_responsavel_por_id(db: Session, responsavel_id: int) -> Optional[Responsavel]:
    return ResponsavelRepository.buscar_por_id(db, responsavel_id)


def listar_responsaveis(db: Session, skip: int = 0, limit: int = 100) -> list[Responsavel]:
    return ResponsavelRepository.listar(db, skip, limit)


def atualizar_responsavel(db: Session, responsvel_id: int, responsavel_in: ResponsavelUpdate) -> Responsavel:
    db_responsavel = ResponsavelRepository.buscar_por_id(db, responsvel_id)
    if not db_responsavel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responsável não encontrado")

    update_data = responsavel_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_responsavel, key, value)

    return ResponsavelRepository.atualizar(db, db_responsavel)


def excluir_responsavel(db: Session, responsavel_id: int) -> None:
    db_responsavel = ResponsavelRepository.buscar_por_id(db, responsavel_id)
    if not db_responsavel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responsável não encontrado")

    ResponsavelRepository.excluir(db, db_responsavel)
