from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.api.dependencies import get_db
from app.schemas.responsavel import ResponsavelResponse, ResponsavelCreate, ResponsavelUpdate
from app.services import responsavel_service

router = APIRouter(prefix="/responsaveis", tags=["Responsáveis"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=ResponsavelResponse, status_code=status.HTTP_201_CREATED)
def criar(responsavel_in: ResponsavelCreate, db: Session = Depends(get_db)):
    return responsavel_service.criar_responsavel(db, responsavel_in)


@router.get("/", response_model=list[ResponsavelResponse])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return responsavel_service.listar_responsaveis(db, skip, limit)


@router.get("/{responsavel_id}", response_model=ResponsavelResponse)
def buscar(responsavel_id: int, db: Session = Depends(get_db)):
    responsavel = responsavel_service.buscar_responsavel_por_id(db, responsavel_id)
    if not responsavel:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responsável não encontrado")
    return responsavel


@router.patch("/{responsavel_id}", response_model=ResponsavelResponse)
def atualizar(responsavel_id: int, responsavel_in: ResponsavelUpdate, db: Session = Depends(get_db)):
    return responsavel_service.atualizar_responsavel(db, responsavel_id, responsavel_in)


@router.delete("/{responsavel_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir(responsavel_id: int, db: Session = Depends(get_db)):
    responsavel_service.excluir_responsavel(db, responsavel_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
