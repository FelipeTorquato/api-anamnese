from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.models import Usuario
from app.schemas.paciente import PacienteCreate, PacienteResponse, PacienteVincularTerapeutas
from app.schemas.paciente import PacienteDetalhadoResponse
from app.services import paciente_service

# Cria o grupo de rotas com um prefixo unificado
router = APIRouter(prefix="/pacientes", tags=["Gestão de Pacientes"], dependencies=[Depends(get_current_user)])


@router.post(
    "/",
    response_model=PacienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo paciente (RF01)"
)
def criar_paciente(
        paciente_in: PacienteCreate,  # O FastAPI converte o JSON recebido para este Schema e valida
        db: Session = Depends(get_db),  # Injeta a sessão do banco de dados
):
    return paciente_service.criar_paciente(db, paciente_in)


@router.get("/", response_model=List[PacienteResponse], summary="Listar pacientes")
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista paginada de pacientes.
    """
    return paciente_service.listar_pacientes(db, skip, limit)


@router.post("/{paciente_id}/terapeutas", response_model=PacienteDetalhadoResponse,
             summary="Vincular terapeutas ao paciente")
def vincular_terapeutas(paciente_id: int, vinculo_in: PacienteVincularTerapeutas, db: Session = Depends(get_db),
                        currernt_user: Usuario = Depends(get_current_user)):
    return paciente_service.vincular_terapeutas(db, paciente_id, vinculo_in.terapeutas_ids)
