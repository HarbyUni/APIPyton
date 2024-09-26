from fastapi import APIRouter, Body
from app.schema.materiales import MaterialSchema, CreateMaterialSchema, FetchMaterialResponse, MaterialResponse, FetchMaterialSchema
from app.controller.materiales import fetch_all_materiales, fetch_material_by_id, create_material, update_material
from app.common.utils import transform_mongo_document
from app.schema.base import build_response
from loguru import logger

router = APIRouter(
    prefix="/material",
    tags=["material"]
)

@router.get(path="/all",
            description="Fetch all materials",
            response_model=FetchMaterialResponse)
async def fetch_materiales():
    try:
        materiales = await fetch_all_materiales()
        material_schemas = [MaterialSchema(**transform_mongo_document(material)) for material in materiales]
        fetch_material_schema = FetchMaterialSchema(Material=material_schemas, total=len(material_schemas))
        return build_response(success=True, data=fetch_material_schema, status_code=200)
    except Exception as e:
        logger.exception("fetch_materiales")
        return build_response(success=False, error="An error occurred while fetching materials", status_code=500)

@router.get(path="/{material_id}",
            description="Get a material by id",
            response_model=MaterialResponse)
async def get_material(material_id: str):
    try:
        material = await fetch_material_by_id(material_id)
        if not material:
            return build_response(success=False, error="No records found", status_code=404)
        material_schema = MaterialSchema(**transform_mongo_document(material))
        return build_response(success=True, data=material_schema, status_code=200)
    except Exception as e:
        logger.exception("get_material")
        return build_response(success=False, error="An error occurred while fetching this material", status_code=500)

@router.post(path="/new",
             description="Create a new material",
             response_model=MaterialResponse)
async def new_material(material: CreateMaterialSchema = Body(...)):
    try:
        material_dict = material.model_dump()
        _id = await create_material(material_dict)
        if _id:
            material_dict["_id"] = _id

        material_schema = MaterialSchema(**transform_mongo_document(material_dict))
        return build_response(success=True, data=material_schema, status_code=200)
    except Exception as e:
        logger.exception("create_material")
        return build_response(success=False, error="An error occurred while creating a new material", status_code=500)

@router.put(path="/update",
            description="Update a material",
            response_model=MaterialResponse)
async def update_material(material: MaterialSchema = Body(...)):
    try:
        material_dict = material.model_dump()
        updated = await update_material(material_dict)
        if not updated:
            return build_response(success=False,
                                  error=f"Material {material_dict['id_material']} was not updated",
                                  status_code=403)

        material_schema = MaterialSchema(**material_dict)
        return build_response(success=True, data=material_schema, status_code=200)
    except Exception as e:
        logger.exception("update_material")
        return build_response(success=False, error="An error occurred while updating the material", status_code=500)
