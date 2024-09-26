from bson.objectid import ObjectId
from app.common.db import db

async def fetch_all_recompensas():
    recompensas = await db.recompensas.find().to_list(1000)
    return recompensas

async def fetch_recompensa_by_id(recompensa_id: str):
    recompensa = await db.recompensas.find_one({"_id": ObjectId(recompensa_id)})
    return recompensa

async def create_recompensa(recompensa_data: dict):
    result = await db.recompensas.insert_one(recompensa_data)
    return result.inserted_id

async def update_recompensa(recompensa_data: dict):
    _id = ObjectId(recompensa_data.pop("id_recompensa"))
    result = await db.recompensas.update_one({"_id": _id}, {"$set": recompensa_data})
    return result.modified_count
