from fastapi import FastAPI
from ..Routes import upload_app
from ..helpers import get_settings

app = FastAPI()
app.include_router(upload_app)
