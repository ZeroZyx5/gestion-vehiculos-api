from fastapi import APIRouter, HTTPException, Query, status
from pymongo import ReturnDocument
from core.database import vehiculos_collection
from schemas.vehiculo import VehiculoCreate, VehiculoResponse, VehiculoUpdate
from utils.mongo import formatear_vehiculo, validar_object_id

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


@router.get(
    "/buscar/placa",
    response_model=VehiculoResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar vehículo por placa",
    description="Busca un vehículo específico mediante su número de placa (búsqueda insensible a mayúsculas/minúsculas).",
)
def buscar_por_placa(placa: str = Query(..., min_length=1, description="Placa del vehículo a buscar")):
    placa_limpia = placa.strip()
    vehiculo = vehiculos_collection.find_one({
        "placa": {"$regex": f"^{placa_limpia}$", "$options": "i"}
    })
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ningún vehículo con la placa '{placa}'."
        )
    return formatear_vehiculo(vehiculo)


@router.get(
    "/filtrar/marca",
    response_model=list[VehiculoResponse],
    status_code=status.HTTP_200_OK,
    summary="Filtrar vehículos por marca",
    description="Retorna la lista de vehículos que coincidan con la marca especificada.",
)
def filtrar_por_marca(marca: str = Query(..., min_length=1, description="Marca del vehículo a filtrar")):
    marca_limpia = marca.strip()
    cursor = vehiculos_collection.find({
        "marca": {"$regex": f"^{marca_limpia}$", "$options": "i"}
    })
    return [formatear_vehiculo(doc) for doc in cursor]


@router.get(
    "/filtrar/tipo",
    response_model=list[VehiculoResponse],
    status_code=status.HTTP_200_OK,
    summary="Filtrar vehículos por tipo",
    description="Retorna la lista de vehículos que coincidan con el tipo especificado (ej: Sedán, SUV, Camioneta).",
)
def filtrar_por_tipo(tipo: str = Query(..., min_length=1, description="Tipo de vehículo a filtrar")):
    tipo_limpio = tipo.strip()
    cursor = vehiculos_collection.find({
        "tipo": {"$regex": f"^{tipo_limpio}$", "$options": "i"}
    })
    return [formatear_vehiculo(doc) for doc in cursor]


@router.get(
    "/{id}",
    response_model=VehiculoResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar un vehículo por identificador",
    description="Busca y obtiene la información detallada de un vehículo a partir de su ID de MongoDB.",
)
def consultar_vehiculo_por_id(id: str):
    obj_id = validar_object_id(id)
    vehiculo = vehiculos_collection.find_one({"_id": obj_id})
    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con ID '{id}' no encontrado."
        )
    return formatear_vehiculo(vehiculo)


@router.put(
    "/{id}",
    response_model=VehiculoResponse,
    status_code=status.HTTP_200_OK,
    summary="Modificar la información de un vehículo",
    description="Actualiza los datos de un vehículo existente mediante su identificador.",
)
def modificar_vehiculo(id: str, vehiculo_in: VehiculoUpdate):
    obj_id = validar_object_id(id)

    vehiculo_existente = vehiculos_collection.find_one({"_id": obj_id})
    if not vehiculo_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con ID '{id}' no encontrado."
        )

    datos_actualizar = vehiculo_in.model_dump(exclude_unset=True, mode="json")

    # Si se actualiza la placa, verificar que no esté duplicada en otro registro
    if "placa" in datos_actualizar:
        nueva_placa = datos_actualizar["placa"].strip().upper()
        duplicado = vehiculos_collection.find_one({
            "_id": {"$ne": obj_id},
            "placa": {"$regex": f"^{nueva_placa}$", "$options": "i"}
        })
        if duplicado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe otro vehículo registrado con la placa '{datos_actualizar['placa']}'."
            )
        datos_actualizar["placa"] = nueva_placa

    if not datos_actualizar:
        return formatear_vehiculo(vehiculo_existente)

    vehiculo_actualizado = vehiculos_collection.find_one_and_update(
        {"_id": obj_id},
        {"$set": datos_actualizar},
        return_document=ReturnDocument.AFTER
    )

    return formatear_vehiculo(vehiculo_actualizado)


@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar un vehículo",
    description="Elimina de forma permanente un vehículo mediante su identificador.",
)
def eliminar_vehiculo(id: str):
    obj_id = validar_object_id(id)
    resultado = vehiculos_collection.delete_one({"_id": obj_id})
    if resultado.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con ID '{id}' no encontrado."
        )
    return {
        "mensaje": "Vehículo eliminado exitosamente",
        "id": id
    }
