from fastapi import APIRouter, Body
from loguru import logger
from app.schema.solicitudesrecoleccion import (
    SolicitudRecoleccionSchema,
    CreateSolicitudSchema,
    FetchSolicitudBody,
    FetchSolicitudResponse,
    FetchSolicitudSchema,
    SolicitudResponse
)
from app.controller.solicitudesrecoleccion import (
    create_solicitud_recoleccion,
    fetch_all_solicitudes_recoleccion,
    fetch_solicitud_recoleccion_by_id,
    update_solicitud_recoleccion
)
from app.common.utils import transform_mongo_document
from app.schema.base import build_response

router = APIRouter(
    prefix="/solicitudes",
    tags=["solicitud_recoleccion"]
)

@router.get("/all", response_model=FetchSolicitudResponse)
async def fetch_solicitudes():
    try:
        solicitudes = await fetch_all_solicitudes_recoleccion()
        solicitudes_schemas = [
            SolicitudRecoleccionSchema(**transform_mongo_document(solicitud))
            for solicitud in solicitudes
        ]
        fetch_solicitudes_schema = FetchSolicitudSchema(
            solicitudes=solicitudes_schemas,
            total=len(solicitudes_schemas)
        )
        return build_response(success=True, data=fetch_solicitudes_schema, status_code=200)
    except Exception as e:
        logger.exception("An error occurred while fetching solicitudes")
        return build_response(success=False, error=str(e), status_code=500)

@router.get("/{solicitud_id}", response_model=SolicitudResponse)
async def get_solicitud(solicitud_id: str):
    try:
        solicitud = await fetch_solicitud_recoleccion_by_id(solicitud_id)
        if not solicitud:
            return build_response(success=False, error="No records found", status_code=404)
        solicitud_schema = SolicitudRecoleccionSchema(**transform_mongo_document(solicitud))
        return build_response(success=True, data=solicitud_schema, status_code=200)
    except Exception as e:
        logger.exception(f"Error fetching solicitud {solicitud_id}")
        return build_response(success=False, error=str(e), status_code=500)

@router.post("/new", response_model=SolicitudResponse)
async def new_solicitud(solicitud: CreateSolicitudSchema = Body(...)):
    try:
        solicitud_dict = solicitud.dict()
        _id = await create_solicitud_recoleccion(solicitud_dict)
        if _id:
            solicitud_dict["id"] = str(_id)
    
        solicitud_schema = SolicitudRecoleccionSchema(**transform_mongo_document(solicitud_dict))
        return build_response(success=True, data=solicitud_schema, status_code=200)
    except Exception as e:
        logger.exception("An error occurred while creating a new solicitud")
        return build_response(success=False, error=str(e), status_code=500)

@router.put("/update", response_model=SolicitudResponse)
async def update_solicitud(solicitud: SolicitudRecoleccionSchema = Body(...)):
    try:
        solicitud_dict = solicitud.dict()
        logger.debug(f"Solicitud recibida para actualización: {solicitud_dict}")

        updated = await update_solicitud_recoleccion(solicitud_dict)

        if not updated:
            logger.warning(f"Solicitud {solicitud_dict['id']} no fue actualizada.")
            return build_response(success=False, error=f"Solicitud {solicitud_dict['id']} not updated", status_code=403)
        
        solicitud_schema = SolicitudRecoleccionSchema(**solicitud_dict)
        return build_response(success=True, data=solicitud_schema, status_code=200)
    except Exception as e:
        logger.exception("Error updating solicitud")
        return build_response(success=False, error=str(e), status_code=500)

