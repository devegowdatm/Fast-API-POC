import shutil
import os

from typing import Optional
from fastapi import Depends, File, UploadFile, Request
from fastapi.responses import HTMLResponse

from core import app, templates
from api import api_router
from config import settings
from models import async_db


@app.on_event("startup")
async def startup():
    await async_db.connect()


@app.on_event("shutdown")
async def shutdown():
    await async_db.disconnect()


# from fastapi.security import OAuth2PasswordBearer
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# from pydantic import BaseModel


# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None


# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     return user


# @app.get("/users/me")
# async def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user


# @app.get("/security")
# async def read_items(token: str=Depends(oauth2_scheme)):
#     return {"token": token}


# # VIEW TO RENDER TEMPLATE.
# @app.get("/", response_class=HTMLResponse, include_in_schema=False)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})


# # ENDPOINT TO UPLOAD FILE.
# @app.post("/upload/", tags=['File upload'])
# async def upload(image: UploadFile=File(...)):
#     with open(
#         os.path.join(settings.STATIC_PATH, 'images', image.filename), "wb"
#     ) as buffer:
#         shutil.copyfileobj(image.file, buffer)
#     return {"filename": image.filename}


# CONFIGURE API ENDPOINTS TO APP.
app.include_router(api_router, prefix="/api")

import json
from fastapi import FastAPI
from starlette.config import Config
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError

# app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="!secret")

config = Config('.env')
print(config)
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@app.route('/')
async def homepage(request: Request):
    import ipdb;ipdb.set_trace()
    return templates.TemplateResponse("index.html", {"request": request})


@app.route('/login')
async def login(request: Request):
    import ipdb;ipdb.set_trace()
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.route('/auth')
async def auth(request: Request):
    import ipdb;ipdb.set_trace()
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    user = await oauth.google.parse_id_token(request, token)
    request.session['user'] = dict(user)
    return RedirectResponse('/')


@app.route('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host='127.0.0.1', port=8000)