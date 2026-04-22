from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate, PacienteResponse

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
        db: Session = Depends(get_db)  # Injeta a sessão do banco de dados
):
    # 1. Evitar duplicidade
    # extrair essa lógica para um Service
    paciente_existente = db.query(Paciente).filter(Paciente.rg == paciente_in.rg).first()
    if paciente_existente:
        # (400 Bad Request)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um paciente cadastrado com este RG."
        )

    # 2. Conversão: Schema (Pydantic) -> Dicionário -> Model (SQLAlchemy)
    # Excluímos 'responsaveis_ids' aqui pois é um relacionamento, trataremos via banco
    dados_paciente = paciente_in.model_dump(exclude={"responsaveis_ids"})
    novo_paciente = Paciente(**dados_paciente)

    # 3. Operações no Banco
    db.add(novo_paciente)
    db.commit()  # Dispara o INSERT
    db.refresh(novo_paciente)  # Atualiza o objeto com os dados gerados pelo banco (ex: ID, created_at)

    # 4. Retorno: O FastAPI pega a Entidade do SQLAlchemy e converte
    # de volta para o PacienteResponse automaticamente (graças ao from_attributes=True)
    return novo_paciente


@router.get("/", response_model=List[PacienteResponse], summary="Listar pacientes")
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna uma lista paginada de pacientes.
    """
    pacientes = db.query(Paciente).offset(skip).limit(limit).all()
    return pacientes
