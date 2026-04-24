from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Usuario, Atendimento, StatusAgenda, Evolucao
from app.repositories.agenda_repository import AgendaRepository
from app.repositories.prontuario_repository import ProntuarioRepository
from app.schemas.prontuario import AtendimentoCreate, EvolucaoCreate


def iniciar_atendimento(db: Session, atendimento_in: AtendimentoCreate, current_user: Usuario) -> Atendimento:
    agenda = AgendaRepository.buscar_por_id(db, atendimento_in.agenda_id)
    if not agenda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado")

    if not current_user.terapeuta or agenda.terapeuta_id != current_user.terapeuta.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas o terapeuta responsável pode iniciar o atendimento")

    agora = datetime.now(timezone.utc)
    inicio_sessao = agenda.data_hora_inicio

    if inicio_sessao.tzinfo is None:
        inicio_sessao = inicio_sessao.replace(tzinfo=timezone.utc)

    if inicio_sessao > agora:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Não é possível iniciar o atendimento antes do horário agendado")

    atendimento_existente = ProntuarioRepository.buscar_atendimento_por_agenda(db, agenda.id)
    if atendimento_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Este agendamento já possui uma ficha de acompanhamento iniciada.")

    agenda.status = StatusAgenda.PRESENTE
    db.commit()

    novo_atendimento = Atendimento(agenda_id=agenda.id)
    return ProntuarioRepository.criar_atendimento(db, novo_atendimento)


def registrar_evolucao(db: Session, atendimento_id: int,
                       evolucao_in: EvolucaoCreate, current_user: Usuario) -> Evolucao:
    atendimento = ProntuarioRepository.buscar_atendimento_por_id(db, atendimento_id)
    if not atendimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atendimento (Ficha) não encontrado")

    if not current_user.terapeuta or atendimento.agenda.terapeuta_id != current_user.terapeuta.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Apenas o terapeuta responsável pela sessão pode registrar a evolução")

    # ver a questão de mais de uma evolução por sessão
    if atendimento.evolucao:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Esse atendimento já possui uma evolução registrada")

    nova_evolucao = Evolucao(
        atendimento_id=atendimento.id,
        descricao=evolucao_in.descricao,
        created_by=current_user.email
    )
    return ProntuarioRepository.criar_evolucao(db, nova_evolucao)
