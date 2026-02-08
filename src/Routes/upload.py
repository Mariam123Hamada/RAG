from fastapi import APIRouter, UploadFile, File
from ..controllers.BaseController import BaseController 
from fastapi import status

upload_app = APIRouter(
    prefix="/API/Upload",
    tags=["RAG/API/Upload"]
)

@upload_app.post("/F_upload" ,status_code=status.HTTP_200_OK)
async def upload_file(file: UploadFile = File(...)):
    file_name = file.filename
    # print(file_name)
    project = BaseController.get_file_extension(filename=file_name)
    return {"file_extension": project}

