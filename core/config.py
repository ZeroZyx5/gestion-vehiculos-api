import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "gestion_vehiculos"
)

if not MONGODB_URI:
    raise ValueError(
        "No se encontró MONGODB_URI en el archivo .env"
    )
