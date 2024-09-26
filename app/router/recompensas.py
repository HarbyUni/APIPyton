from fastapi import APIRouter, Body
from app.schema.recompensas import (RecompensaSchema, CreateRecompensasSchema, FetchRecompensasSchema, FetchRecompensasResponse, RecompensaResponse)
from app.controller.recompensas import (fetch_all_recompensas, fetch_recompensa_by_id, create_recompensa, update_recompensa)
from app.common.utils import transform_mongo_document
from app.schema.base import build_response
from loguru import logger

router = APIRouter(
    prefix="/recompensa",
    tags=["recompensa"]
)

@router.get(path="/all",
            description="Fetch all recompensas",
            response_model=FetchRecompensasResponse)
async def fetch_recompensas():
    try:
        recompensas = await fetch_all_recompensas()
        recompensa_schemas = [RecompensaSchema(**transform_mongo_document(recompensa)) for recompensa in recompensas]
        fetch_recompensas_schema = FetchRecompensasSchema(perfiles=recompensa_schemas, total=len(recompensa_schemas))
        return build_response(success=True, data=fetch_recompensas_schema, status_code=200)
    except Exception as e:
        logger.exception("fetch_recompensas")
        return build_response(success=False, error="An error occurred while fetching recompensas", status_code=500)

@router.get(path="/{recompensa_id}",
            description="Get a recompensa by id",
            response_model=RecompensaResponse)
async def get_recompensa(recompensa_id: str):
    try:
        recompensa = await fetch_recompensa_by_id(recompensa_id)
        if not recompensa:
            return build_response(success=False, error="No records found", status_code=404)
        recompensa_schema = RecompensaSchema(**transform_mongo_document(recompensa))
        return build_response(success=True, data=recompensa_schema, status_code=200)
    except Exception as e:
        logger.exception("get_recompensa")
        return build_response(success=False, error="An error occurred while fetching this recompensa", status_code=500)

@router.post(path="/new",
             description="Create a new recompensa",
             response_model=RecompensaResponse)
async def new_recompensa(recompensa: CreateRecompensasSchema = Body(...)):
    try:
        recompensa_dict = recompensa.model_dump()
        _id = await create_recompensa(recompensa_dict)
        if _id:
            recompensa_dict["_id"] = _id

        recompensa_schema = RecompensaSchema(**transform_mongo_document(recompensa_dict))
        return build_response(success=True, data=recompensa_schema, status_code=200)
    except Exception as e:
        logger.exception("create_recompensa")
        return build_response(success=False, error="An error occurred while creating a new recompensa", status_code=500)

@router.put(path="/update",
            description="Update a recompensa",
            response_model=RecompensaResponse)
async def update_recompensa(recompensa: RecompensaSchema = Body(...)):
    try:
        recompensa_dict = recompensa.model_dump()
        updated = await update_recompensa(recompensa_dict)
        if not updated:
            return build_response(success=False,
                                  error=f"Recompensa {recompensa_dict['id_recompensa']} was not updated",
                                  status_code=403)

        recompensa_schema = RecompensaSchema(**recompensa_dict)
        return build_response(success=True, data=recompensa_schema, status_code=200)
    except Exception as e:
        logger.exception("update_recompensa")
        return build_response(success=False, error="An error occurred while updating the recompensa", status_code=500)
