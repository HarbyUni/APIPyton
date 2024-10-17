from passlib.context import CryptContext
from fastapi import HTTPException, Request
from app.security import verify_password
from app.controller.usuarios import fetch_usuario_by_id
from app.common.db import db


# Configuración de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Base de datos simple en memoria (debería ser reemplazada por una base de datos real)
fake_db = {}

# Función para hashear contraseñas
def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Registro de nuevo usuario
async def register_user(username: str, password: str):
    if username in db:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    hashed_password = hash_password(password)
    fake_db[username] = {"username": username, "password": hashed_password}
    return {"message": "Usuario registrado con éxito"}


async def login_user(request: Request, email: str, password: str):
    usuario = await db.usuarios.find_one({"email": email})
    
    if not usuario or not verify_password(password, usuario['hashed_password']):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")
    
    # Guardar información del usuario en la sesión
    request.session['user'] = {
        'id': str(usuario['_id']),
        'email': usuario['email'],
        'nombres': usuario.get('nombres'),
        'apellidos': usuario.get('apellidos'),
        # Otros campos si los necesitas
    }
    
    return {"message": "Login exitoso", "user": request.session['user']}
