from fastapi import APIRouter, Body
from app.schema.centrosacopio import (CentroAcopiochema, CreateCentroAcopiochemaSchema, FetchCentroAcopiochemaResponse, CentroAcopiochemaResponse)
from app.controller.centrosacopio import (fetch_all_centros_acopio, fetch_centro_acopio_by_id, create_centro_acopio, update_centro_acopio)
from app.common.utils import transform_mongo_document
from app.schema.base import build_response
from loguru import logger

router = APIRouter(
    prefix="/centro_acopio",
    tags=["centro_acopio"]
)

@router.get(path="/all",
            description="Fetch all centros de acopio",
            response_model=FetchCentroAcopiochemaResponse)
async def fetch_centros_acopio():
    try:
        centros = await fetch_all_centros_acopio()
        centro_schemas = [CentroAcopiochema(**transform_mongo_document(centro)) for centro in centros]
        fetch_centros_schema = FetchCentroAcopiochemaSchema(Material=centro_schemas, total=len(centro_schemas))
        return build_response(success=True, data=fetch_centros_schema, status_code=200)
    except Exception as e:
        logger.exception("fetch_centros_acopio")
        return build_response(success=False, error="An error occurred while fetching centros de acopio", status_code=500)

@router.get(path="/{centro_id}",
            description="Get a centro de acopio by id",
            response_model=CentroAcopiochemaResponse)
async def get_centro_acopio(centro_id: str):
    try:
        centro = await fetch_centro_acopio_by_id(centro_id)
        if not centro:
            return build_response(success=False, error="No records found", status_code=404)
        centro_schema = CentroAcopiochema(**transform_mongo_document(centro))
        return build_response(success=True, data=centro_schema, status_code=200)
    except Exception as e:
        logger.exception("get_centro_acopio")
        return build_response(success=False, error="An error occurred while fetching this centro de acopio", status_code=500)

@router.post(path="/new",
             description="Create a new centro de acopio",
             response_model=CentroAcopiochemaResponse)
async def new_centro_acopio(centro: CreateCentroAcopiochemaSchema = Body(...)):
    try:
        centro_dict = centro.model_dump()
        _id = await create_centro_acopio(centro_dict)
        if _id:
            centro_dict["_id"] = _id

        centro_schema = CentroAcopiochema(**transform_mongo_document(centro_dict))
        return build_response(success=True, data=centro_schema, status_code=200)
    except Exception as e:
        logger.exception("create_centro_acopio")
        return build_response(success=False, error="An error occurred while creating a new centro de acopio", status_code=500)

@router.put(path="/update",
            description="Update a centro de acopio",
            response_model=CentroAcopiochemaResponse)
async def update_centro_acopio(centro: CentroAcopiochema = Body(...)):
    try:
        centro_dict = centro.model_dump()
        updated = await update_centro_acopio(centro_dict)
        if not updated:
            return build_response(success=False,
                                  error=f"Centro {centro_dict['id_centro']} was not updated",
                                  status_code=403)

        centro_schema = CentroAcopiochema(**centro_dict)
        return build_response(success=True, data=centro_schema, status_code=200)
    except Exception as e:
        logger.exception("update_centro_acopio")
        return build_response(success=False, error="An error occurred while updating the centro de acopio", status_code=500)
