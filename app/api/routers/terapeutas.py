from typing import List

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.api.dependencies import get_db
from app.schemas.terapeuta import TerapeutaResponse, TerapeutaCreate
from app.services import terapeuta_service

router = APIRouter(prefix="/terapeutas", tags=["Gestão de Equipe"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=TerapeutaResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_terapeuta(terapeuta_in: TerapeutaCreate, db: Session = Depends(get_db)):
    return terapeuta_service.criar_terapeuta(db, terapeuta_in)


@router.get("/", response_model=List[TerapeutaResponse])
def listar_terapeutas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return terapeuta_service.listar_terapeutas(db, skip, limit)


@router.get("/{terapeuta_id}", response_model=TerapeutaResponse)
def buscar_terapeuta(terapeuta_id: int, db: Session = Depends(get_db)):
    return terapeuta_service.buscar_terapeuta(db, terapeuta_id)
