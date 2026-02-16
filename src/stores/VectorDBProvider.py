from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from fastapi import UploadFile 
from typing import List

class VectorDBProvider(ABC):
    def __init__(
        self,
        db_client,
        embed_size: int,
        distance_method: str
    ):
        self.db_client = db_client
        self.embed_size = embed_size
        self.distance_method = distance_method

    @abstractmethod
    async def connect(self, db: Session):
        pass

    @abstractmethod
    async def disconnect(self):
        pass


    @abstractmethod
    async def insert_project(self, file: UploadFile):
        pass

    @abstractmethod
    async def search(self, query_vector: List[float], top_k: int = 5):
        pass
    
    
    @abstractmethod
    async def get_collection_info(self, project_id: int):
        pass 
