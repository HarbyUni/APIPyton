from fastapi import APIRouter, Depends, Request, HTTPException
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

# Dependencia que verifica si el usuario está autenticado
async def get_current_user(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="No autenticado")
    return user

# Ruta protegida, solo para usuarios autenticados
@api_router.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"¡Hola, {user['username']}! Estás autenticado."}

# Incluye otros routers
api_router.include_router(product)
api_router.include_router(usuarios)
api_router.include_router(perfil)
api_router.include_router(material)
api_router.include_router(recompensas)
api_router.include_router(registroreciclaje)
api_router.include_router(centro_acopio)
