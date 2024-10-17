from fastapi import FastAPI, Request
from starlette.requests import Request
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
import time
from app.router.api import api_router
from app.router import login  # Autenticación Google
from app.router import auth_basic  # Autenticación básicamportar tu archivo login

app = FastAPI(
    title="Reciclapp"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware de sesiones
app.add_middleware(SessionMiddleware, secret_key="vvcamkhbasjyajsakajadsnbubjksmmkssxicdaanns")



# Incluye el router de login
app.include_router(login.router)  # Autenticación Google
app.include_router(auth_basic.router)  # Autenticación básica
app.include_router(api_router)

# Ruta para "/"
@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a Reciclapp!"}

# Middleware para agregar tiempo de procesamiento en la cabecera
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:0.4f} sec"
    return response
