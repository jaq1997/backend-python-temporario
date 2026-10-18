from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import questionario, estabelecimentos

# Cria as tabelas no PostgreSQL caso não existam
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="InformaSaúde API",
    description="Backend para triagem de saúde (jornadas) e busca geolocalizada de UPAs e Hospitais.",
    version="1.0.0",
)

# Configuração de CORS para permitir requisições do frontend React (Vite: 5173 / 3000)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(questionario.router)
app.include_router(estabelecimentos.router)


@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "ok", "app": "InformaSaúde API"}
