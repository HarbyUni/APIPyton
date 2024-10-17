from fastapi import APIRouter, Form, Request, Depends
from starlette.responses import HTMLResponse, RedirectResponse
from app.controller.auth_basic import register_user, login_user

router = APIRouter(
    prefix="/auth-basic",
    tags=["auth-basic"]
)

# Ruta para registro
@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    return await register_user(username, password)

# Ruta para inicio de sesión

@router.post("/login")
async def basic_auth_login(request: Request, email: str = Form(...), password: str = Form(...)):
    result = await login_user(request, email, password)
    return result


# Ruta para formulario de registro
@router.get("/register", response_class=HTMLResponse)
async def show_register_form():
    return HTMLResponse("""
    <form action="/auth-basic/register" method="post">
        <input type="text" name="username" placeholder="Nombre de usuario"/>
        <input type="password" name="password" placeholder="Contraseña"/>
        <button type="submit">Registrar</button>
    </form>
    """)

# Ruta para formulario de inicio de sesión
@router.get("/login", response_class=HTMLResponse)
async def show_login_form():
    return HTMLResponse("""
    <form action="/auth-basic/login" method="post">
        <input type="text" name="username" placeholder="Nombre de usuario"/>
        <input type="password" name="password" placeholder="Contraseña"/>
        <button type="submit">Iniciar sesión</button>
    </form>
    """)
