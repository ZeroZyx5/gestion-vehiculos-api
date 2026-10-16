from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Propietario(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre completo del propietario")
    telefono: str = Field(..., min_length=5, max_length=20, description="Teléfono de contacto")


class PropietarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, min_length=5, max_length=20)


class Mantenimiento(BaseModel):
    fecha: str = Field(..., description="Fecha del mantenimiento en formato YYYY-MM-DD", pattern=r"^\d{4}-\d{2}-\d{2}$")
    descripcion: str = Field(..., min_length=1, max_length=300, description="Detalle del trabajo realizado")
    costo: float = Field(..., ge=0, description="Costo del mantenimiento")


class VehiculoCreate(BaseModel):
    placa: str = Field(..., min_length=1, max_length=15, description="Placa única del vehículo")
    marca: str = Field(..., min_length=1, max_length=50, description="Marca del vehículo (ej: Toyota, Nissan)")
    modelo: str = Field(..., min_length=1, max_length=50, description="Modelo del vehículo (ej: Corolla, Sentra)")
    anio: int = Field(..., ge=1886, le=2100, description="Año de fabricación")
    tipo: str = Field(..., min_length=1, max_length=50, description="Tipo de vehículo (ej: Sedán, SUV, Camioneta)")
    color: str = Field(..., min_length=1, max_length=30, description="Color del vehículo")
    estado: str = Field(..., min_length=1, max_length=30, description="Estado (ej: Activo, En mantenimiento, Inactivo)")
    mantenimientos: list[Mantenimiento] = Field(default_factory=list, description="Lista de mantenimientos registrados")
    propietario: Propietario = Field(..., description="Datos del propietario")


class VehiculoUpdate(BaseModel):
    placa: Optional[str] = Field(None, min_length=1, max_length=15)
    marca: Optional[str] = Field(None, min_length=1, max_length=50)
    modelo: Optional[str] = Field(None, min_length=1, max_length=50)
    anio: Optional[int] = Field(None, ge=1886, le=2100)
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, min_length=1, max_length=30)
    estado: Optional[str] = Field(None, min_length=1, max_length=30)
    mantenimientos: Optional[list[Mantenimiento]] = None
    propietario: Optional[PropietarioUpdate] = None


class VehiculoResponse(VehiculoCreate):
    id: str = Field(alias="_id", description="Identificador único generado por MongoDB")

    model_config = ConfigDict(populate_by_name=True)
