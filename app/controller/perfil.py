from bson.objectid import ObjectId
from app.common.db import db


async def fetch_all_perfiles_usuario():
    perfiles = await db.perfil_usuario.find().to_list(1000)
    return perfiles

async def fetch_perfil_usuario_by_id(perfil_id: str):
    perfil = await db.perfil_usuario.find_one({"_id": ObjectId(perfil_id)})
    return perfil

async def create_perfil_usuario(perfil_data: dict):
    result = await db.perfil_usuario.insert_one(perfil_data)
    return result.inserted_id

async def update_perfil_usuario(perfil_data: dict):
    _id = ObjectId(perfil_data.pop("id"))
    result = await db.perfil_usuario.update_one({"_id": _id}, {"$set": perfil_data})
    return result.modified_count



