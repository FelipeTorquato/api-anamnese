from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models import Agenda
from app.models import StatusAgenda


class AgendaRepository:

    @staticmethod
    def verificar_conflito_terapeuta(db: Session, terapeuta_id: int, inicio: datetime,
                                     fim: datetime) -> Optional[Agenda]:
        return db.query(Agenda).filter(
            Agenda.terapeuta_id == terapeuta_id,
            Agenda.data_hora_inicio < fim,
            Agenda.data_hora_fim > inicio,
            Agenda.status != StatusAgenda.CANCELADO
        ).first()

    @staticmethod
    def verificar_conflito_paciente(db: Session, paciente_id: int, inicio: datetime,
                                    fim: datetime) -> Optional[Agenda]:
        return db.query(Agenda).filter(
            Agenda.paciente_id == paciente_id,
            Agenda.data_hora_inicio < fim,
            Agenda.data_hora_fim > inicio,
            Agenda.status != StatusAgenda.CANCELADO
        ).first()

    @staticmethod
    def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Agenda]:
        return db.query(Agenda).offset(skip).limit(limit).all()

    @staticmethod
    def criar(db: Session, agenda: Agenda) -> Agenda:
        db.add(agenda)
        db.commit()
        db.refresh(agenda)
        return agenda

    @staticmethod
    def buscar_por_id(db: Session, agenda_id: int) -> Optional[Agenda]:
        return db.query(Agenda).filter(Agenda.id == agenda_id).first()
