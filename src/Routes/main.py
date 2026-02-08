from fastapi import FastAPI
from .upload import upload_app

app = FastAPI()
app.include_router(upload_app)
