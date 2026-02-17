from ...helpers import  get_settings , get_db
from ..embedding import cohereProvider
from ..generation import grokgenertion
from fastapi import APIRouter, UploadFile, File, Depends, status 
from ...models import ProjectSplitters
from sqlalchemy.orm import Session
from ...stores.providers import pgvector
from ...controllers import BaseController


class NLPTask:
    def __init__(self):
        self.splitter = None
        self.client = None
        self.db_service = None
        self.embed = None

    def initialize_providers(self, db: Session):
        settings = get_settings

        grok_key = settings.GROK_KEY
        cohere_key = settings.COHERE_KEY

        if not grok_key:
            raise ValueError("Grok Key is not provided.")

        if not cohere_key:
            raise ValueError("Cohere Key is not provided.")

        if not db:
            raise RuntimeError("Database session is not provided.")

        self.client = grokgenertion(api_key=grok_key , genertion_model=settings.GENERTION_MODEL)
        self.client.connect()

        self.embed = cohereProvider(api_key=cohere_key)
        self.splitter = ProjectSplitters()
        self.db_service = pgvector(self.splitter, db)

    async def upload_file(self, file: UploadFile):
        if not file:
            raise RuntimeError("File is not provided.")

        if not self.splitter:
            raise RuntimeError("Splitter is not initialized.")

        if not self.db_service:
            raise RuntimeError("Database service is not initialized.")

        file_extension = BaseController.get_file_extension(file.filename)
        result = await self.db_service.insert_project(file)
        # this is teh content of result 
        #     "project_id": new_project.project_id,
        #     "chunks_saved": len(data_chunks)
        # }
        return {
            "file_extension": file_extension,
            "status": "success",
            "data": result["project_id"] ,
            "total_chunks" : result["chunks_saved"]
        }

    async def search_vector(self, project_id: int, query_vector):
        if not project_id:
            raise ValueError("Project ID is not provided.")

        if not query_vector:
            raise ValueError("Query vector is not provided.")

        if not self.db_service:
            raise RuntimeError("Database connection is not initialized.")

        return self.db_service.search(query_vector=query_vector, top_k=5)

    def answer_question(self, project_id: int, text: str):
        if not text:
            raise ValueError("Question text is required.")

        # Step 1: Convert text to embedding
        query_vector = self.embed.embed_text(text)

        # Step 2: Retrieve relevant chunks
        chunks = self.search_vector(project_id, query_vector)

        if not chunks:
            return {"result": "No relevant context found."}

        # Step 3: Build RAG prompt
        context = "\n".join([chunk["content"] for chunk in chunks])

        # Step 4: Generate answer
        result = self.client.chat_models(
                    question=text,
                    chunks=context
           )

        return {
            "result": "Success",
            "answer": result
        }

