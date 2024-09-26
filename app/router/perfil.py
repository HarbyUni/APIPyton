from fastapi import APIRouter, Body
from app.schema.perfil import PerfilUsuarioSchema , CreatePerfilUsuarioSchema, FetchPerfilesUsuarioSchema, PerfilUsuarioResponse, FetchPerfilesUsuarioResponse
from app.controller.perfil import fetch_all_perfiles_usuario, fetch_perfil_usuario_by_id, create_perfil_usuario, update_perfil_usuario
from app.common.utils import transform_mongo_document
from app.schema.base import build_response

router = APIRouter(
    prefix="/perfil_usuario",
    tags=["perfil_usuario"]
)

@router.get(path="/all",
            description="Fetch all perfiles de usuario",
            response_model=FetchPerfilesUsuarioResponse)
async def fetch_perfiles_usuario():
    try:
        perfiles = await fetch_all_perfiles_usuario()
        perfil_schemas = [PerfilUsuarioSchema(**transform_mongo_document(perfil)) for perfil in perfiles]
        fetch_perfiles_schema = FetchPerfilesUsuarioSchema(perfiles=perfil_schemas, total=len(perfil_schemas))
        return build_response(success=True, data=fetch_perfiles_schema, status_code=200)
    except Exception:
        return build_response(success=False, error="An error occurred while fetching perfiles de usuario", status_code=500)

@router.get(path="/{perfil_id}",
            description="Get a perfil de usuario by id",
            response_model=PerfilUsuarioResponse)
async def get_perfil_usuario(perfil_id: str):
    try:
        perfil = await fetch_perfil_usuario_by_id(perfil_id)
        if not perfil:
            return build_response(success=False, error="No records found", status_code=404)
        perfil_schema = PerfilUsuarioSchema(**transform_mongo_document(perfil))
        return build_response(success=True, data=perfil_schema, status_code=200)
    except Exception:
        return build_response(success=False, error="An error occurred while fetching this perfil de usuario", status_code=500)

@router.post(path="/new",
             description="Create a new perfil de usuario",
             response_model=PerfilUsuarioResponse)
async def new_perfil_usuario(perfil: CreatePerfilUsuarioSchema = Body(...)):
    try:
        perfil_dict = perfil.model_dump()
        _id = await create_perfil_usuario(perfil_dict)
        if _id:
            perfil_dict["_id"] = _id

        perfil_schema = PerfilUsuarioSchema(**transform_mongo_document(perfil_dict))
        return build_response(success=True, data=perfil_schema, status_code=200)
    except Exception:
        return build_response(success=False, error="An error occurred while creating a new perfil de usuario", status_code=500)

@router.put(path="/update",
            description="Update a perfil de usuario",
            response_model=PerfilUsuarioResponse)
async def update_perfil_usuario(perfil: PerfilUsuarioSchema = Body(...)):
    try:
        perfil_dict = perfil.model_dump()
        updated = await update_perfil_usuario(perfil_dict)
        if not updated:
            return build_response(success=False,
                                  error=f"perfil {perfil_dict['id']} was not updated",
                                  status_code=403)

        perfil_schema = PerfilUsuarioSchema(**perfil_dict)
        return build_response(success=True, data=perfil_schema, status_code=200)
    except Exception:
        return build_response(success=False, error="An error occurred while updating a perfil de usuario", status_code=500)
