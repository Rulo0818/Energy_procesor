from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.routes import archivos, energia, errores, stats
from app.database import get_db


app = FastAPI(
    title="API Procesamiento Peajes - Energía Excedentaria",
    description="Sistema de carga y consulta de archivos de energía excedentaria",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(archivos.router)
app.include_router(energia.router)
app.include_router(errores.router)
app.include_router(stats.router)


@app.get("/")
def root():
    return {"service": "energy-process", "docs": "/docs"}
