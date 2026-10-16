from fastapi import APIRouter, HTTPException, status
from core.database import vehiculos_collection
from schemas.vehiculo import VehiculoCreate, VehiculoResponse
from utils.mongo import formatear_vehiculo

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])


@router.post(
    "",
    response_model=VehiculoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo vehículo",
    description="Crea un nuevo registro de vehículo en la colección. La placa debe ser única.",
)
def registrar_vehiculo(vehiculo_in: VehiculoCreate):
    # Verificar si la placa ya existe (búsqueda normalizada a mayúsculas)
    placa_limpia = vehiculo_in.placa.strip().upper()
    vehiculo_existente = vehiculos_collection.find_one({"placa": {"$regex": f"^{placa_limpia}$", "$options": "i"}})
    if vehiculo_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un vehículo registrado con la placa '{vehiculo_in.placa}'."
        )

    datos = vehiculo_in.model_dump(mode="json")
    datos["placa"] = placa_limpia
    resultado = vehiculos_collection.insert_one(datos)
    datos["_id"] = resultado.inserted_id

    return formatear_vehiculo(datos)


@router.get(
    "",
    response_model=list[VehiculoResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los vehículos",
    description="Obtiene la lista completa de todos los vehículos registrados.",
)
def listar_vehiculos():
    cursor = vehiculos_collection.find()
    return [formatear_vehiculo(doc) for doc in cursor]
