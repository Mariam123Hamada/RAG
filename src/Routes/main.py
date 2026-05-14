from fastapi import FastAPI
from .DataRoute import upload_app
from ..helpers import get_settings
from ..utils.metrics import setup_metrics


app = FastAPI()
setup_metrics(app)
app.include_router(upload_app)
