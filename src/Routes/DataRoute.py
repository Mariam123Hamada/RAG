from fastapi import APIRouter, UploadFile, File, Depends, status
from sqlalchemy.orm import Session
from ..helpers import get_db
from ..stores.providers.PGVECTOR import pgvector
from ..models import ProjectSplitters
from ..controllers.BaseController import BaseController

from ..servicies.tasks.NLPTask import NLPTask
upload_app = APIRouter(
    prefix="/API/Upload",
    tags=["RAG/API/Upload"]
)

# Dependency to get a pgvector instance
# def get_pgvector_service(db: Session = Depends(get_db)) -> pgvector:
#     splitter = ProjectSplitters(chunk_size=500, chunk_overlap=50)
#     vector_service = pgvector(splitter=splitter, db=db)
#     return vector_service


def get_nlp_task(db:Session =Depends(get_db)):
    nlp_task=NLPTask()
    nlp_task.initialize_providers(db=db)
    return nlp_task
    
    
@upload_app.post("/F_upload",description="This Endpoint is used For the Upload File ", status_code=status.HTTP_201_CREATED)
async def upload_file(
    file: UploadFile = File(...),
    service: NLPTask = Depends(get_nlp_task)
):
    """
    Upload a file, split it into chunks, and save it to PostgreSQL using pgvector.
    """

    result=  await service.upload_file(file)

    
    return {
        "status": "success",
        "data": result
    }

@upload_app.post("/Asnwer_Questions" , description="This Endpoint is used for Answer the question." , status_code = status.HTTP_200_OK)
async def answer(project_id:int , text : str , service:NLPTask = Depends(get_nlp_task)):
    """ This is the Answer Question Endpoint """
    
    answer = service.answer_question(project_id , text)
    return {
        "answer" : answer["answer"]
    }    
