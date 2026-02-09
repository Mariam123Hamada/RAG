from VectorDBProvider import VectorDBProvider
import sqlalchemy import select
from sqlalchemy.exc.session  import sessionmaker


class pgvector(VectorDBProvider):
    async def connect(self , db_client):
        self.db_client=db_client


    async def disconnect(self):
        pass


    async def create_collection(
        self,
        collection_name: str,
        do_reset: bool = False
    ):
        pass 
                

    async def delete_collection(
        self,
        collection_name: str
    ):
        pass

    async def insert_chunks(
        self,
        collection_name: str,
        vectors: list,
        metadatas: list,
        ids: list
    ):
        pass

    async def search(
        self,
        collection_name: str,
        query_vector: list,
        top_k: int
    ):
        pass

    async def get_collection_info(
        self,
        collection_name: str
    ):
        pass
