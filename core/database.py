from pymongo import MongoClient
from core.config import MONGODB_URI, MONGODB_DATABASE

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=5000
)

database = client[MONGODB_DATABASE]

vehiculos_collection = database["vehiculos"]


def verificar_conexion():
    client.admin.command("ping")
    return True
