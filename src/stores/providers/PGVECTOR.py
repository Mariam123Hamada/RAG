from typing import List
from fastapi import UploadFile
from sqlalchemy.orm  import Session
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from ...models import DataChunk
from ...models import ProjectSplitters
from ...stores.schemas import ProjectSchema, ChunkSchema
from ...helpers import get_db , get_settings
from ...stores import VectorDBInterface
from ...servicies.embedding import cohereProvider

class pgvector(VectorDBInterface):
    def __init__(self, splitter: ProjectSplitters, db: AsyncSession = None):
        """
        Args:
            splitter: Your ProjectSplitters instance to handle file reading & splitting
            db: SQLAlchemy AsyncSession
        """
        self.db = db
        self.splitter = splitter
        self.embed_client=None

    async def connect(self, db: AsyncSession):
        """Assign the SQLAlchemy session"""
        self.db = db
        app = get_settings
        coher_api=app.COHERE_KEY
        self.embed_client=cohereProvider(api_key=coher_api).connect()

    async def disconnect(self):
        """Disconnect the session"""
        self.db = None

    async def insert_project(self, project_id, file: UploadFile):
        """
        Read file, split into chunks, store project metadata in 'projects' table
        and chunks in 'chunks' table with embeddings initialized to zeros.
        """
        
        if not self.db:
            raise RuntimeError("Database session is not connected.")
        #The get() method only works for the Primary Key.
        existing_pro_id = await self.db.get(ProjectSchema , project_id)
        if existing_pro_id:
            return {
                "status":"Skipped" , 
                "Description": f"The Project With this id is not allowed{project_id} , Change the project id"
            }
        else:          
            # Read file and extract text
            text = await self.splitter.read_file(file)
            project_name = self.splitter.create_project_name(file.filename)
            
            # Split text into chunks
            chunks_text = await self.splitter.make_splitting(text)
            data_chunks = await self.splitter.make_DataChunk_Split(chunks_text , project_id=2000)
            
            # Insert into projects table
            new_project = ProjectSchema(
                total_chunks=len(data_chunks),
                project_id=project_id , 
                project_name=project_name
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

        
            await self.db.commit()

            return {
                "status":"sucess",
                "project_id": new_project.project_id,
                "Project_name" : project_name ,
                "chunks_saved": len(data_chunks)
            }
    async def search(self, query_vector, top_k = 5):
        if not self.db :
            raise RuntimeError("DataBase is Not Conected.")
        
        stmt = select(ChunkSchema).order_by(
            ChunkSchema.embedding.l2_distance(query_vector)
        ).limit(top_k)
        result = await self.db.execute(stmt)
        # print(type(result))  -> <class 'sqlalchemy.engine.result.ChunkedIteratorResult'>
        # print(result)  -> <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x0000016156595E90>
        res=result.scalars().all()
        # print(type(res)) ->List 
        # print(res) 
        context = "\n".join([chunk.content for chunk in res])
        return context
    async def get_collection_info(self, project_id):
        """ This Function return the info about the cllection file  """
        if self.db is None:
            raise RuntimeError("DataBAsel is not called")
        
        stmt = select(ProjectSchema).where(ProjectSchema.project_id == project_id)
        result = await self.db.execute(stmt)
        project = result.scalars().first()
        if project is None :
            return None 
        else :
            return {
            "project id":project.project_id ,
            "# chunks":project.total_chunks
        }    
   