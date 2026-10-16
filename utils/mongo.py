from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status


def validar_object_id(id_str: str) -> ObjectId:
    """
    Valida y convierte un string a ObjectId de MongoDB.
    Si el formato es incorrecto, lanza un error HTTP 400.
    """
    try:
        return ObjectId(id_str)
    except (InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El identificador '{id_str}' no es un ObjectId válido de MongoDB"
        )


def formatear_vehiculo(doc: dict) -> dict:
    """
    Transforma un documento de MongoDB para que coincida con el schema de respuesta:
    convierte _id en string para id/_id.
    """
    if not doc:
        return doc
    doc["_id"] = str(doc["_id"])
    return doc
