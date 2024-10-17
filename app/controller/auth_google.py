# app/controller/auth_google.py
from authlib.integrations.starlette_client import OAuth
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from os import getenv
from app.common.constants import Env

# Configurar OAuth
oauth = OAuth()

# Registrar cliente de Google
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_id=getenv(Env.GOOGLE.CLIENT_ID),
    client_secret=getenv(Env.GOOGLE.CLIENT_SECRET),
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account',  # Fuerza a seleccionar una cuenta
    }
)

# Función para manejar el login
async def google_login(request: Request):
    redirect_uri = getenv(Env.GOOGLE.GOOGLE_REDIRECT_URI)
    print(redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

# Función para manejar el callback de autenticación
async def google_auth_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    if user:
        request.session['user'] = user
    return RedirectResponse(url='/api')

# Función para manejar el logout
async def google_logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
