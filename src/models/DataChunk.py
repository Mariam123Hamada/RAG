from fastapi import UploadFile 
import pypdf 
from typing import List
 

class DataChunk:
    def __init__(self, content: str, project_id: str , embedding:List):
        self.content = content
        self.project_id = project_id
        self.embedding=embedding
           
        