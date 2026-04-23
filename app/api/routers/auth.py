from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.core import security
from app.repositories.usuario_repository import UsuarioRepository

router = APIRouter(prefix="/auth", tags=["Autenticação"])


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = UsuarioRepository.buscar_por_email(db, email=form_data.username)
    if not usuario or not security.verify_password(form_data.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(
        data={"sub": usuario.email, "perfil": usuario.perfil.value}
    )

    return {"access_token": access_token, "token_type": "bearer"}
