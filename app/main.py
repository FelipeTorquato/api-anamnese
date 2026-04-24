from fastapi import FastAPI

# Cria as tabelas no banco de dados se elas não existirem
# IMPORTANTE: Você precisa importar todos os models antes de rodar isso
# (por isso aquele nosso __init__.py na pasta models é vital)
import app.models
from app.api.routers import prontuarios
from app.api.dependencies import engine
from app.api.routers import agendas
from app.api.routers import auth
from app.api.routers import pacientes, responsaveis
from app.api.routers import terapeutas
from app.api.routers import usuarios
from app.models.base import Base

Base.metadata.create_all(bind=engine)

# Inicializa a aplicação
app = FastAPI(
    title="API de Gestão Clínica",
    description="Sistema para gestão de pacientes, terapeutas e prontuários.",
    version="1.0.0"
)

# Registra os nossos Controllers (Routers)
app.include_router(pacientes.router)
app.include_router(responsaveis.router)
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(terapeutas.router)
app.include_router(agendas.router)
app.include_router(prontuarios.router)


@app.get("/", tags=["Health Check"])
def root():
    return {"status": "online", "message": "API Clínica operante."}
