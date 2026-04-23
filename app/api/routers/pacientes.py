from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.schemas.paciente import PacienteCreate, PacienteResponse
from app.services import paciente_service
from app.models import Usuario

# Cria o grupo de rotas com um prefixo unificado
router = APIRouter(prefix="/pacientes", tags=["Gestão de Pacientes"])


@router.post(
    "/",
    response_model=PacienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar novo paciente (RF01)"
)
def criar_paciente(
        paciente_in: PacienteCreate,  # O FastAPI converte o JSON recebido para este Schema e valida
        db: Session = Depends(get_db),  # Injeta a sessão do banco de dados
        current_user: Usuario = Depends(get_current_user)
):
    return paciente_service.criar_paciente(db, paciente_in)


@router.get("/", response_model=List[PacienteResponse], summary="Listar pacientes")
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista paginada de pacientes.
    """
    return paciente_service.listar_pacientes(db, skip, limit)
