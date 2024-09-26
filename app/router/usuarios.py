from fastapi import APIRouter, Body
from app.schema.usuarios import UsuarioSchema, CreateUsuarioSchema, FetchUsuariosSchema, FetchUsuariosResponse, UsuarioResponse
from app.controller.usuarios import fetch_all_usuarios, fetch_usuario_by_id, create_usuario, update_usuario
from app.common.utils import transform_mongo_document
from app.schema.base import build_response

router = APIRouter(
    prefix="/usuario",
    tags=["usuario"]
)

@router.get(path="/all",
            description="Fetch all usuarios",
            response_model=FetchUsuariosResponse)
async def fetch_usuarios():
    try:
        usuarios = await fetch_all_usuarios()
        usuario_schemas = [UsuarioSchema(**transform_mongo_document(usuario)) for usuario in usuarios]
        fetch_usuarios_schema = FetchUsuariosSchema(usuarios=usuario_schemas, total=len(usuario_schemas))
        return build_response(success=True, data=fetch_usuarios_schema, status_code=200)
    except Exception:
        return build_response(success=False, error="An error occurred while fetching usuarios", status_code=500)

@router.get(path="/{usuario_id}",
            description="Get a usuario by id",
            response_model=UsuarioResponse)
async def get_usuario(usuario_id: str):
    try:
        usuario = await fetch_usuario_by_id(usuario_id)
        if not usuario:
            return build_response(success=False, error="No records found", status_code=404)
        usuario_schema = UsuarioSchema(**transform_mongo_document(usuario))
        return build_response(success=True, data=usuario_schema, status_code=200)
    except Exception:
        return build_response(success=False, error="An error occurred while fetching this usuario", status_code=500)

@router.post(path="/new",
             description="Create a new usuario",
             response_model=UsuarioResponse)
async def new_usuario(usuario: CreateUsuarioSchema = Body(...)):
    try:
        usuario_dict = usuario.model_dump()
        _id = await create_usuario(usuario_dict)
        if _id:
            usuario_dict["_id"] = _id

        usuario_schema = UsuarioSchema(**transform_mongo_document(usuario_dict))
        return build_response(success=True, data=usuario_schema, status_code=200)
    except Exception:
        return build_response(success=False, error="An error occurred while creating a new usuario", status_code=500)

@router.put(path="/update",
            description="Update a usuario",
            response_model=UsuarioResponse)
async def update_usuario(usuario: UsuarioSchema = Body(...)):
    try:
        usuario_dict = usuario.model_dump()
        updated = await update_usuario(usuario_dict)
        if not updated:
            return build_response(success=False,
                                  error=f"usuario {usuario_dict['id']} was not updated",
                                  status_code=403)

        usuario_schema = UsuarioSchema(**usuario_dict)
        return build_response(success=True, data=usuario_schema, status_code=200)
    except Exception:
        return build_response(success=False, error="An error occurred while updating a usuario", status_code=500)
