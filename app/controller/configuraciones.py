from bson.objectid import ObjectId
from app.common.db import db


async def fetch_all_configuraciones():
    configuraciones = await db.configuraciones.find().to_list(1000)
    return configuraciones

async def fetch_configuracion_by_id(configuracion_id: str):
    configuracion = await db.configuraciones.find_one({"_id": ObjectId(configuracion_id)})
    return configuracion

async def create_configuracion(configuracion_data: dict):
    result = await db.configuraciones.insert_one(configuracion_data)
    return result.inserted_id

async def update_configuracion(configuracion_data: dict):
    _id = ObjectId(configuracion_data.pop("id"))
    result = await db.configuraciones.update_one({"_id": _id}, {"$set": configuracion_data})
    return result.modified_count
