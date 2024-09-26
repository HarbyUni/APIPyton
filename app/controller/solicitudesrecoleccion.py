from bson.objectid import ObjectId
from app.common.db import db


async def fetch_all_solicitudes_recoleccion():
    solicitudes = await db.solicitudes_recoleccion.find().to_list(1000)
    return solicitudes

async def fetch_solicitud_recoleccion_by_id(solicitud_id: str):
    solicitud = await db.solicitudes_recoleccion.find_one({"_id": ObjectId(solicitud_id)})
    return solicitud

async def create_solicitud_recoleccion(solicitud_data: dict):
    result = await db.solicitudes_recoleccion.insert_one(solicitud_data)
    return result.inserted_id

async def update_solicitud_recoleccion(solicitud_data: dict):
    _id = ObjectId(solicitud_data.pop("id"))
    result = await db.solicitudes_recoleccion.update_one({"_id": _id}, {"$set": solicitud_data})
    return result.modified_count
