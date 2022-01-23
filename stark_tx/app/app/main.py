from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers.main import router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)
