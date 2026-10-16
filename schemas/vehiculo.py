from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class Propietario(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    telefono: str = Field(min_length=5, max_length=20)


class Mantenimiento(BaseModel):
    fecha: date
    descripcion: str = Field(min_length=1, max_length=300)
    costo: float = Field(ge=0)


class VehiculoCreate(BaseModel):
    placa: str = Field(min_length=1, max_length=15)
    marca: str = Field(min_length=1, max_length=50)
    modelo: str = Field(min_length=1, max_length=50)
    anio: int = Field(ge=1886, le=2100)
    tipo: str = Field(min_length=1, max_length=50)
    color: str = Field(min_length=1, max_length=30)
    estado: str = Field(min_length=1, max_length=30)
    mantenimientos: list[Mantenimiento] = Field(default_factory=list)
    propietario: Propietario


class VehiculoResponse(VehiculoCreate):
    id: str = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True)
