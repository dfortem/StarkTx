from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routes.main import router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)


# Set all CORS enabled origins
app = CORSMiddleware(
    app=app,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
