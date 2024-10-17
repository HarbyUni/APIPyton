from bson.objectid import ObjectId
from app.common.db import db
from app.security import hash_password  # Importa la función de hashing

async def fetch_all_usuarios():
    usuarios = await db.usuarios.find().to_list(1000)
    return usuarios

async def fetch_usuario_by_id(usuario_id: str):
    usuario = await db.usuarios.find_one({"_id": ObjectId(usuario_id)})
    return usuario

async def create_usuario(usuario_data: dict):
    # Hashear la contraseña antes de guardarla en la base de datos
    usuario_data['hashed_password'] = hash_password(usuario_data.pop('password'))
    result = await db.usuarios.insert_one(usuario_data)
    return result.inserted_id

async def update_usuario(usuario_data: dict):
    _id = ObjectId(usuario_data.pop("id"))
    result = await db.usuarios.update_one({"_id": _id}, {"$set": usuario_data})
    return result.modified_count
