from fastapi import FastAPI
from api.v1.router import api_router

app = FastAPI(
    title="Gestión de Vehículos API",
    description=(
        "API REST para administrar vehículos "
        "y sus historiales de mantenimiento."
    ),
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def inicio():
    return {
        "mensaje": "API de Gestión de Vehículos funcionando",
        "documentacion": "/docs",
    }
