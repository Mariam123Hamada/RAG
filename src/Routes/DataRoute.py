from fastapi import APIRouter, UploadFile, File, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..helpers import get_db
from ..stores.providers.PGVECTOR import pgvector
from ..models import ProjectSplitters
from ..controllers.BaseController import BaseController
from ..servicies.tasks.NLPTask import NLPTask
upload_app = APIRouter(
    prefix="/RAG",
    tags=["RAG/API/Upload"]
)

def get_nlp_task(db:AsyncSession =Depends(get_db)):
    nlp_task=NLPTask()
    nlp_task.initialize_providers(db=db)
    return nlp_task
    
    
@upload_app.post("/FileUpload",description="This Endpoint is used For the Upload File ", status_code=status.HTTP_201_CREATED)
async def upload_file(
    project_id : int ,
    file: UploadFile = File(...),
    service: NLPTask = Depends(get_nlp_task)
):
    """
    Upload a file, split it into chunks, and save it to PostgreSQL using pgvector.
    """

    result=  await service.upload_file(project_id,file)

    
    return {
        "status": "success",
        "data": result
    }

@upload_app.post("/AsnwerQuestions" , description="This Endpoint is used for Answer the question." , status_code = status.HTTP_200_OK)
async def answer(project_id:int , text : str , service:NLPTask = Depends(get_nlp_task)):
    """ This is the Answer Question Endpoint """
    
    answer = await service.answer_question(project_id , text)
    return {
        "answer" : answer["answer"]
    }    


@upload_app.post("/Reterivechunks" , description="This is teh Endpoint to show teh retriver chunks related to the quesry vector" , status_code=status.HTTP_200_OK)    
async def reterivier(project_id , text : str , service:NLPTask = Depends(get_nlp_task)):
    res= await service.search_vector(project_id , text )
    return  {
        "res":res
    }