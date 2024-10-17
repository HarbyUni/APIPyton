# app/router/login.py
from fastapi import APIRouter, Request
from app.controller import auth_google  # Importa el controlador

router = APIRouter()

@router.get("/login")
async def login(request: Request):
    return await auth_google.google_login(request)

@router.get("/auth/google/callback")
async def auth(request: Request):
    return await auth_google.google_auth_callback(request)

@router.get("/logout")
async def logout(request: Request):
    return await auth_google.google_logout(request)

