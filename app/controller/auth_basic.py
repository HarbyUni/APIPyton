from passlib.context import CryptContext
from fastapi import HTTPException, Request
from app.security import verify_password
from app.common.db import db

# Configuración de bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para hashear contraseñas
def hash_password(password: str):
    return pwd_context.hash(password)

# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Registro de nuevo usuario
async def register_user(username: str, password: str):
    usuario = await db.usuarios.find_one({"username": username})
    
    if usuario:
        raise HTTPException(status_code=400, detail="El usuario ya existe.")
    
    hashed_password = hash_password(password)
    new_user = {"username": username, "hashed_password": hashed_password}
    
    # Inserta el nuevo usuario en la base de datos
    await db.usuarios.insert_one(new_user)
    
    return {"message": "Usuario registrado con éxito"}

async def login_user(request: Request, email: str, password: str):
    usuario = await db.usuarios.find_one({"email": email})

    # Verificar si el usuario existe
    if not usuario:
        raise HTTPException(status_code=400, detail="El usuario no existe.")
    
    # Verificar si la contraseña es correcta
    if not verify_password(password, usuario['hashed_password']):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas.")
    
    # Guardar información del usuario en la sesión, si request no es None
    if request:
        request.session['user'] = {
            'id': str(usuario['_id']),
            'email': usuario['email'],
            'nombres': usuario.get('nombres'),
            'apellidos': usuario.get('apellidos'),
        }
        user_data = request.session['user']
    else:
        user_data = {
            'id': str(usuario['_id']),
            'email': usuario['email'],
            'nombres': usuario.get('nombres'),
            'apellidos': usuario.get('apellidos'),
        }

    return {"message": "Login exitoso", "user": user_data}


