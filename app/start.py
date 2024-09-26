# app/start.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import time
from app.router.api import api_router
from app.common.constants import Env

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

# Ruta para "/"
@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a Reciclapp!"}

# Incluye tu api_router
app.include_router(api_router)

# Middleware y eventos adicionales
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:0.4f} sec"
    return response
