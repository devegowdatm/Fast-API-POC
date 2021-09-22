from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import settings

# INIT APP
app = FastAPI(
    title=settings.APP_NAME, description=settings.DESCRIPTION,
    version=settings.VERSION)

# MOUNT STATIC FOLDER.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create a templates object.
templates = Jinja2Templates(directory="templates")
