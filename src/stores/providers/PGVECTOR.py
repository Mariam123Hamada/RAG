from typing import List
from fastapi import UploadFile
from sqlalchemy.orm  import Session
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from ...models import DataChunk
from ...models import ProjectSplitters
from ...stores.schemas import ProjectSchema, ChunkSchema
from ...helpers import get_db , get_settings
from ...stores import VectorDBProvider 
from ...servicies.embedding import cohereProvider


class pgvector(VectorDBProvider):
    def __init__(self, splitter: ProjectSplitters, db: Session = None):
        """
        Args:
            splitter: Your ProjectSplitters instance to handle file reading & splitting
            db: SQLAlchemy Session
        """
        self.db = db
        self.splitter = splitter
        self.embed_client=None

    async def connect(self, db: Session):
        """Assign the SQLAlchemy session"""
        self.db = db
        app = get_settings
        coher_api=app.COHERE_KEY
        self.embed_client=cohereProvider(api_key=coher_api).connect()

    async def disconnect(self):
        """Disconnect the session"""
        self.db = None

    async def insert_project(self, file: UploadFile):
        """
        Read file, split into chunks, store project metadata in 'projects' table
        and chunks in 'chunks' table with embeddings initialized to zeros.
        """
        
        if not self.db:
            raise RuntimeError("Database session is not connected.")

        # Read file and extract text
        text = await self.splitter.read_file(file)
        # project_name = self.splitter.create_project_name(file.filename)
        project_name=5522
        # Split text into chunks
        chunks_text = await self.splitter.make_splitting(text)
        data_chunks = await self.splitter.make_DataChunk_Split(chunks_text , project_id=2000)

        # Insert into projects table
        new_project = ProjectSchema(
            total_chunks=len(data_chunks),
            project_id=project_name
        )
        self.db.add(new_project)
        self.db.flush()  

        #  Insert chunks
        for i, chunk in enumerate(data_chunks):
            db_chunk = ChunkSchema(
                project_id=new_project.project_id,
                content=chunk.content,
                embedding=chunk.embedding 
            )
            self.db.add(db_chunk)

       
        self.db.commit()

        return {
            "project_id": new_project.project_id,
            "chunks_saved": len(data_chunks)
        }
    async def search(self, query_vector, top_k = 5):
        if not self.db :
            raise RuntimeError("DataBase is Not Conected.")
        
        stmt = select(ChunkSchema).order_by(
            ChunkSchema.embedding.l2_distance(query_vector)
        ).limit(top_k)
        result = self.db.execute(stmt)
        return result.scalers().all()        
    async def get_collection_info(self, project_id):
        """ This Function return the info about the cllection file  """
        if self.db is None:
            raise RuntimeError("DataBAsel is not called")
        
        project = self.db.query(ProjectSchema).filter_by(project_id=project_id).first()
        if project is None :
            return None 
        else :
            return {
            "project id":project.project_id ,
            "# chunks":project.total_chunks
        }    
   