from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models import Terapeuta


class TerapeutaRepository:

    @staticmethod
    def buscar_por_id(db: Session, terapeuta_id: int) -> Optional[Terapeuta]:
        return db.query(Terapeuta).filter(Terapeuta.id == terapeuta_id).filter(Terapeuta.deleted_at.is_(None)).first()

    @staticmethod
    def buscar_por_usuario_id(db: Session, usuario_id: int) -> Optional[Terapeuta]:
        return db.query(Terapeuta).filter(Terapeuta.usuario_id == usuario_id).filter(
            Terapeuta.deleted_at.is_(None)).first()

    @staticmethod
    def buscar_por_ids(db: Session, ids: List[int]) -> List[Terapeuta]:
        return db.query(Terapeuta).filter(Terapeuta.id.in_(ids)).filter(Terapeuta.deleted_at.is_(None)).all()

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Terapeuta]:
        return db.query(Terapeuta).filter(Terapeuta.deleted_at.is_(None)).offset(skip).limit(limit).all()

    @staticmethod
    def criar(db: Session, terapeuta: Terapeuta) -> Terapeuta:
        db.add(terapeuta)
        db.commit()
        db.refresh(terapeuta)
        return terapeuta

    @staticmethod
    def excluir(db: Session, terapeuta: Terapeuta) -> None:
        terapeuta.deleted_at = datetime.now(timezone.utc)
        db.commit()
