from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.usuario import UsuarioResponse, UsuarioCreate
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.criar_usuario(db, usuario_in)