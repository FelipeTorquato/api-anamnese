from typing import Optional

from sqlalchemy.orm import Session

from app.models import Atendimento, Evolucao


class ProntuarioRepository:

    @staticmethod
    def buscar_atendimento_por_agenda(db: Session, agenda_id: int) -> Optional[Atendimento]:
        return db.query(Atendimento).filter(Atendimento.agenda_id == agenda_id).first()

    @staticmethod
    def buscar_atendimento_por_id(db: Session, atendimento_id: int) -> Optional[Atendimento]:
        return db.query(Atendimento).filter(Atendimento.id == atendimento_id).first()

    @staticmethod
    def criar_atendimento(db: Session, atendimento: Atendimento) -> Atendimento:
        db.add(atendimento)
        db.commit()
        db.refresh(atendimento)
        return atendimento

    @staticmethod
    def criar_evolucao(db: Session, evolucao: Evolucao) -> Evolucao:
        db.add(evolucao)
        db.commit()
        db.refresh(evolucao)
        return evolucao
