from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.responsavel import Responsavel


class ResponsavelRepository:

    @staticmethod
    def buscar_por_id(db: Session, responsavel_id: int) -> Optional[Responsavel]:
        return db.query(Responsavel).filter(Responsavel.id == responsavel_id).filter(
            Responsavel.deleted_at.is_(None)).first()

    @staticmethod
    def buscar_por_cpf(db: Session, cpf: str) -> Optional[Responsavel]:
        return db.query(Responsavel).filter(Responsavel.cpf == cpf).filter(Responsavel.deleted_at.is_(None)).first()

    @staticmethod
    def buscar_por_ids(db: Session, ids: List[int]) -> List[Responsavel]:
        return db.query(Responsavel).filter(Responsavel.id.in_(ids)).filter(Responsavel.deleted_at.is_(None)).all()

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Responsavel]:
        return db.query(Responsavel).offset(skip).limit(limit).filter(Responsavel.deleted_at.is_(None)).all()

    @staticmethod
    def criar(db: Session, responsavel: Responsavel) -> Responsavel:
        db.add(responsavel)
        db.commit()
        db.refresh(responsavel)
        return responsavel

    @staticmethod
    def atualizar(db: Session, responsavel: Responsavel) -> Responsavel:
        db.commit()
        db.refresh(responsavel)
        return responsavel

    @staticmethod
    def excluir(db: Session, responsavel=Responsavel) -> None:
        responsavel.deleted_at = datetime.now(timezone.utc)
        db.commit()
