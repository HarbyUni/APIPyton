from bson.objectid import ObjectId
from app.common.db import db

async def fetch_all_centros_acopio():
    centros = await db.centros_acopio.find().to_list(1000)
    return centros

async def fetch_centro_acopio_by_id(centro_id: str):
    centro = await db.centros_acopio.find_one({"_id": ObjectId(centro_id)})
    return centro

async def create_centro_acopio(centro_data: dict):
    result = await db.centros_acopio.insert_one(centro_data)
    return result.inserted_id

async def update_centro_acopio(centro_data: dict):
    _id = ObjectId(centro_data.pop("id_centro"))
    result = await db.centros_acopio.update_one({"_id": _id}, {"$set": centro_data})
    return result.modified_count


