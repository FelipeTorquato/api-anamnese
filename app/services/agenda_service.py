from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Agenda
from app.repositories.paciente_repository import PacienteRepository
from app.schemas.agenda import AgendaCreate
from app.repositories.agenda_repository import AgendaRepository
from app.repositories.terapeuta_repository import TerapeutaRepository


def agendar_sessao(db: Session, agenda_in: AgendaCreate) -> Agenda:

    if agenda_in.data_hora_fim <= agenda_in.data_hora_inicio:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O horário de fim deve ser posterior ao horário de início")

    paciente = PacienteRepository.buscar_por_id(db, agenda_in.paciente_id)
    if not paciente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Paciente não encontrado")

    terapeuta = TerapeutaRepository.buscar_por_id(db, agenda_in.terapeuta_id)
    if not terapeuta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Terapeuta não encontrado")

    conflito_terapeuta = AgendaRepository.verificar_conflito_terapeuta(db, terapeuta.id, agenda_in.data_hora_inicio,
                                                                       agenda_in.data_hora_fim)

    if conflito_terapeuta:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="O terapeuta já possui um atendimento neste horário")

    conflito_paciente = AgendaRepository.verificar_conflito_paciente(db, paciente.id, agenda_in.data_hora_inicio,
                                                                     agenda_in.data_hora_fim)

    if conflito_paciente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="O paciente já possui um atendimento neste horário")

    nova_agenda = Agenda(**agenda_in.model_dump())
    return AgendaRepository.criar(db, nova_agenda)


def listar_agendamentos(db: Session, skip: int = 0, limit: int = 100) -> List[Agenda]:
    return AgendaRepository.listar(db, skip, limit)
