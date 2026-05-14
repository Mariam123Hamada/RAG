from ...helpers import  get_settings , get_db
from ...servicies.embedding import cohereProvider , geminiProvider
from ...servicies.generation import grokgenertion
from fastapi import APIRouter, UploadFile, File, Depends, status 
from ...models import ProjectSplitters
from sqlalchemy.ext.asyncio import AsyncSession
from ...stores.providers import pgvector
from ...controllers import BaseController

class NLPTask:
    def __init__(self):
        self.splitter = None
        self.client = None
        self.db_service = None
        self.embed = None

    def initialize_providers(self, db: AsyncSession):
        settings = get_settings

        grok_key = settings.GROK_KEY
        gemmni_key = settings.GEMMNI_KEY

        if not grok_key:
            raise ValueError("Grok Key is not provided.")

        if not gemmni_key:
            raise ValueError("Gemmeni Key is not provided.")

        if not db:
            raise RuntimeError("Database session is not provided.")

        self.client = grokgenertion(api_key=grok_key , genertion_model=settings.GENERTION_MODEL)
        self.client.connect()

        # self.embed = cohereProvider(api_key=cohere_key)
        self.embed = geminiProvider(api_key= gemmni_key)
        self.embed.connect()
        self.splitter = ProjectSplitters()
        self.db_service = pgvector(self.splitter, db)

    async def upload_file(self,project_id , file: UploadFile):
        if not file:
            raise RuntimeError("File is not provided.")

        if not self.splitter:
            raise RuntimeError("Splitter is not initialized.")

        if not self.db_service:
            raise RuntimeError("Database service is not initialized.")

        file_extension = BaseController.get_file_extension(file.filename)
        result = await self.db_service.insert_project(project_id,file)
        
        if result["status"] == "Skipped":
            return result
        
        return {
            "status": "success",
            "file_extension": file_extension,
            "File ID": result["project_id"] ,
            "File Name":result["Project_name"],
            "total_chunks" : result["chunks_saved"]
        }

    async def search_vector(self, project_id: int, query_vector):
        if not project_id:
            raise ValueError("Project ID is not provided.")

        if not query_vector:
            raise ValueError("Query vector is not provided.")

        if not self.db_service:
            raise RuntimeError("Database connection is not initialized.")
        if not isinstance(query_vector , list):
            query_vector=self.embed.embed_text(query_vector)[0].values
        res = await self.db_service.search(query_vector=query_vector, top_k=5)
        return res
    async def answer_question(self, project_id: int, text: str):
        if not text:
            raise ValueError("Question text is required.")

        # Step 1: Convert text to embedding
        query_vector = self.embed.embed_text(text)[0].values

        # Step 2: Retrieve relevant chunks
        # i have handle the methods search vector to return the chunk content not the embedding vector 
        chunks = await self.search_vector(project_id, query_vector)

        if not chunks:
            return {"result": "No relevant context found."}

        
        

        # Step 4: Generate answer
        result = self.client.chat_models(
                    question=text,
                    chunks=chunks
           )

        return {
            "result": "Success",
            "answer": result
        }

