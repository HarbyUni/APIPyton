from fastapi import APIRouter, Body
from app.schema.registroreciclaje import (RegistroReciclajeSchema, CreateRegistroReciclajeSchema, FetchRegistroReciclajeResponse, RegistroReciclajeResponse)
from app.controller.registroreciclaje import (fetch_all_registros_reciclaje, fetch_registro_reciclaje_by_id, create_registro_reciclaje, update_registro_reciclaje)
from app.common.utils import transform_mongo_document
from app.schema.base import build_response
from loguru import logger

router = APIRouter(
    prefix="/registro_reciclaje",
    tags=["registro_reciclaje"]
)

@router.get(path="/all",
            description="Fetch all registros de reciclaje",
            response_model=FetchRegistroReciclajeResponse)
async def fetch_registros_reciclaje():
    try:
        registros = await fetch_all_registros_reciclaje()
        registro_schemas = [RegistroReciclajeSchema(**transform_mongo_document(registro)) for registro in registros]
        fetch_registros_schema = FetchRegistroReciclajeSchema(Registros=registro_schemas, total=len(registro_schemas))
        return build_response(success=True, data=fetch_registros_schema, status_code=200)
    except Exception as e:
        logger.exception("fetch_registros_reciclaje")
        return build_response(success=False, error="An error occurred while fetching registros de reciclaje", status_code=500)

@router.get(path="/{registro_id}",
            description="Get a registro de reciclaje by id",
            response_model=RegistroReciclajeResponse)
async def get_registro_reciclaje(registro_id: str):
    try:
        registro = await fetch_registro_reciclaje_by_id(registro_id)
        if not registro:
            return build_response(success=False, error="No records found", status_code=404)
        registro_schema = RegistroReciclajeSchema(**transform_mongo_document(registro))
        return build_response(success=True, data=registro_schema, status_code=200)
    except Exception as e:
        logger.exception("get_registro_reciclaje")
        return build_response(success=False, error="An error occurred while fetching this registro de reciclaje", status_code=500)

@router.post(path="/new",
             description="Create a new registro de reciclaje",
             response_model=RegistroReciclajeResponse)
async def new_registro_reciclaje(registro: CreateRegistroReciclajeSchema = Body(...)):
    try:
        registro_dict = registro.model_dump()
        _id = await create_registro_reciclaje(registro_dict)
        if _id:
            registro_dict["_id"] = _id

        registro_schema = RegistroReciclajeSchema(**transform_mongo_document(registro_dict))
        return build_response(success=True, data=registro_schema, status_code=200)
    except Exception as e:
        logger.exception("create_registro_reciclaje")
        return build_response(success=False, error="An error occurred while creating a new registro de reciclaje", status_code=500)

@router.put(path="/update",
            description="Update a registro de reciclaje",
            response_model=RegistroReciclajeResponse)
async def update_registro_reciclaje(registro: RegistroReciclajeSchema = Body(...)):
    try:
        registro_dict = registro.model_dump()
        updated = await update_registro_reciclaje(registro_dict)
        if not updated:
            return build_response(success=False,
                                  error=f"Registro {registro_dict['id_registro']} was not updated",
                                  status_code=403)

        registro_schema = RegistroReciclajeSchema(**registro_dict)
        return build_response(success=True, data=registro_schema, status_code=200)
    except Exception as e:
        logger.exception("update_registro_reciclaje")
        return build_response(success=False, error="An error occurred while updating the registro de reciclaje", status_code=500)
