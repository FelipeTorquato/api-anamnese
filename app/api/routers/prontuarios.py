from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.api.dependencies import get_db
from app.models import Usuario
from app.schemas.prontuario import AtendimentoResponse, AtendimentoCreate, EvolucaoCreate
from app.services import prontuario_service
from app.schemas.prontuario import EvolucaoResponse

router = APIRouter(prefix="/prontuarios", tags=["Prontuário Terapêutico"], dependencies=[Depends(get_current_user)])


@router.post("/atendimentos", response_model=AtendimentoResponse, status_code=status.HTTP_201_CREATED)
def iniciar_atendimento(atendimento_in: AtendimentoCreate, db: Session = Depends(get_db),
                        current_user: Usuario = Depends(get_current_user)):
    return prontuario_service.iniciar_atendimento(db, atendimento_in, current_user)


@router.post("/atendimentos/{atendimento_id}/evolucoes", response_model=EvolucaoResponse,
             status_code=status.HTTP_201_CREATED)
def registrar_evolucao(atendimento_id: int, evolucao_in: EvolucaoCreate, db: Session = Depends(get_db),
                       current_user: Usuario = Depends(get_current_user)):
    return prontuario_service.registrar_evolucao(db, atendimento_id, evolucao_in, current_user)
