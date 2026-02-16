from fastapi import FastAPI
from ..Routes import upload_app

app = FastAPI()
app.include_router(upload_app)
