from fastapi import FastAPI
from fastapi.params import Depends

# Cria as tabelas no banco de dados se elas não existirem
# IMPORTANTE: Você precisa importar todos os models antes de rodar isso
# (por isso aquele nosso __init__.py na pasta models é vital)
import app.models
from app.api.dependencies import engine, get_current_user
from app.api.routers import auth
from app.api.routers import pacientes, responsaveis
from app.models.base import Base

Base.metadata.create_all(bind=engine)

# Inicializa a aplicação
app = FastAPI(
    title="API de Gestão Clínica",
    description="Sistema para gestão de pacientes, terapeutas e prontuários.",
    version="1.0.0",
    dependencies=[Depends(get_current_user)]
)

# Registra os nossos Controllers (Routers)
app.include_router(pacientes.router)
app.include_router(responsaveis.router)
app.include_router(auth.router)


@app.get("/", tags=["Health Check"])
def root():
    return {"status": "online", "message": "API Clínica operante."}
