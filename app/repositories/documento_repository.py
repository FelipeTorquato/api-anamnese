from typing import List

from sqlalchemy.orm import Session

from app.models import Documento


class DocumentoRepository:

    @staticmethod
    def criar(db: Session, documento: Documento) -> Documento:
        db.add(documento)
        db.commit()
        db.refresh(documento)
        return documento

    @staticmethod
    def listar_por_paciente(db: Session, paciente_id: int) -> List[Documento]:
        return db.query(Documento).filter(Documento.paciente_id == paciente_id, Documento.deleted_at.is_(None)).all()
