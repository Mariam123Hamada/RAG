from fastapi import APIRouter, UploadFile, File, Depends, status
from sqlalchemy.orm import Session
from ..helpers import get_db
from ..stores.providers.PGVECTOR import pgvector
from ..models import ProjectSplitters
from ..controllers.BaseController import BaseController

upload_app = APIRouter(
    prefix="/API/Upload",
    tags=["RAG/API/Upload"]
)

# Dependency to get a pgvector instance
def get_pgvector_service(db: Session = Depends(get_db)) -> pgvector:
    splitter = ProjectSplitters(chunk_size=500, chunk_overlap=50)
    vector_service = pgvector(splitter=splitter, db=db)
    return vector_service

@upload_app.post("/F_upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    service: pgvector = Depends(get_pgvector_service)
):
    """
    Upload a file, split it into chunks, and save it to PostgreSQL using pgvector.
    """

   
    file_name = file.filename
    file_extension = BaseController.get_file_extension(filename=file_name)

    
    result = await service.insert_project(file=file)

    
    return {
        "file_extension": file_extension,
        "status": "success",
        "data": result
    }
