from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/health")
def health():
    return {"estado": "activo"}
