from bson.objectid import ObjectId
from app.common.db import db

async def fetch_all_registros_reciclaje():
    registros = await db.registros_reciclaje.find().to_list(1000)
    return registros

async def fetch_registro_reciclaje_by_id(registro_id: str):
    registro = await db.registros_reciclaje.find_one({"_id": ObjectId(registro_id)})
    return registro

async def create_registro_reciclaje(registro_data: dict):
    result = await db.registros_reciclaje.insert_one(registro_data)
    return result.inserted_id

async def update_registro_reciclaje(registro_data: dict):
    _id = ObjectId(registro_data.pop("id_registro"))
    result = await db.registros_reciclaje.update_one({"_id": _id}, {"$set": registro_data})
    return result.modified_count
