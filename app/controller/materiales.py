from bson.objectid import ObjectId
from app.common.db import db

async def fetch_all_materiales():
    materiales = await db.materiales.find().to_list(1000)
    return materiales

async def fetch_material_by_id(material_id: str):
    material = await db.materiales.find_one({"_id": ObjectId(material_id)})
    return material

async def create_material(material_data: dict):
    result = await db.materiales.insert_one(material_data)
    return result.inserted_id

async def update_material(material_data: dict):
    _id = ObjectId(material_data.pop("id_material"))
    result = await db.materiales.update_one({"_id": _id}, {"$set": material_data})
    return result.modified_count

