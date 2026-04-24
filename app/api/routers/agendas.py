from typing import List

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.schemas.agenda import AgendaResponse, AgendaCreate
from app.services import agenda_service

router = APIRouter(prefix="/agendas", tags=["Agendas"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=AgendaResponse, status_code=status.HTTP_201_CREATED)
def agendar(agenda_in: AgendaCreate, db: Session = Depends(get_db)):
    return agenda_service.agendar_sessao(db, agenda_in)


@router.get("/", response_model=List[AgendaResponse])
def listar_agendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return agenda_service.listar_agendamentos(db, skip, limit)
