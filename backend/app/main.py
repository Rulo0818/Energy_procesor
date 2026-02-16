from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.api.routes import archivos, energia, errores, stats, usuarios, clientes, auth
from app.database import get_db

# Desactivar logs de SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

app = FastAPI(
    title="API Procesamiento Peajes - Energía Excedentaria v1",
    description="Sistema de carga y consulta de archivos de energía excedentaria",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(archivos.router)
app.include_router(energia.router)
app.include_router(errores.router, prefix="/api/v1/errores")
app.include_router(stats.router)
app.include_router(usuarios.router, prefix="/api/v1/usuarios", tags=["usuarios"])
app.include_router(clientes.router, prefix="/api/v1/clientes", tags=["clientes"])


@app.get("/")
def root():
    return {"service": "energy-process", "docs": "/docs"}, {"message": "Hello World"}