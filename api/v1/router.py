from fastapi import APIRouter
from api.v1.endpoints.vehiculos import router as vehiculos_router

api_router = APIRouter()

api_router.include_router(vehiculos_router)


@api_router.get("/health", tags=["Salud"])
def health():
    return {"estado": "activo"}
