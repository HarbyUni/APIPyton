from fastapi import APIRouter

from app.router.product import router as product
from app.router.usuarios import router as usuarios
from app.router.perfil import router as perfil
from app.router.material import router as material
from app.router.recompensas import router as recompensas
from app.router.registroreciclaje import router as registroreciclaje
from app.router.centrosacopio import router as centro_acopio

api_router = APIRouter(
    prefix="/api",
    responses={
        404: {"description": "Not found"},
        408: {"description": "Timeout"}
        }
    )

#api_router.include_router(product)
api_router.include_router(usuarios)
api_router.include_router(perfil)
api_router.include_router(material)
api_router.include_router(recompensas)
api_router.include_router(registroreciclaje)
api_router.include_router(centro_acopio)
