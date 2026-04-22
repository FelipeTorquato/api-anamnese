from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.paciente import Paciente


class PacienteRepository:

    @staticmethod
    def buscar_por_id(db: Session, paciente_id: int) -> Optional[Paciente]:
        return db.query(Paciente).filter(Paciente.id == paciente_id).first()

    @staticmethod
    def buscar_por_rg(db: Session, rg: str) -> Optional[Paciente]:
        return db.query(Paciente).filter(Paciente.rg == rg).first()

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Paciente]:
        return db.query(Paciente).offset(skip).limit(limit).all()

    @staticmethod
    def criar(db: Session, paciente: Paciente) -> Paciente:
        db.add(paciente)
        db.commit()
        db.refresh(paciente)
        return paciente

    @staticmethod
    def atualizar(db: Session, paciente: Paciente) -> Paciente:
        db.commit()
        db.refresh(paciente)
        return paciente
