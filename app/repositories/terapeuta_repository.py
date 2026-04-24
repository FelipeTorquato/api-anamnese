from typing import Optional, List

from sqlalchemy.orm import Session

from app.models import Terapeuta


class TerapeutaRepository:

    @staticmethod
    def buscar_por_id(db: Session, terapeuta_id: int) -> Optional[Terapeuta]:
        return db.query(Terapeuta).filter(Terapeuta.id == terapeuta_id).first()

    @staticmethod
    def buscar_por_usuario_id(db: Session, usuario_id: int) -> Optional[Terapeuta]:
        return db.query(Terapeuta).filter(Terapeuta.usuario_id == usuario_id).first()

    @staticmethod
    def buscar_por_ids(db: Session, ids: List[int]) -> List[Terapeuta]:
        return db.query(Terapeuta).filter(Terapeuta.id.in_(ids)).all()

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 100) -> list[Terapeuta]:
        return db.query(Terapeuta).offset(skip).limit(limit).all()

    @staticmethod
    def criar(db: Session, terapeuta: Terapeuta) -> Terapeuta:
        db.add(terapeuta)
        db.commit()
        db.refresh(terapeuta)
        return terapeuta

    @staticmethod
    def excluir(db: Session, terapeuta: Terapeuta) -> None:
        db.delete(terapeuta)
        db.commit()
