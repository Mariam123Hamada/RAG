from abc import ABC, abstractmethod


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
    async def connect(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def create_collection(
        self,
        collection_name: str,
        do_reset: bool = False
    ):
        pass

    @abstractmethod
    async def delete_collection(
        self,
        collection_name: str
    ):
        pass

    @abstractmethod
    async def insert_chunks(
        self,
        collection_name: str,
        vectors: list,
        metadatas: list,
        ids: list
    ):
        pass

    @abstractmethod
    async def search(
        self,
        collection_name: str,
        query_vector: list,
        top_k: int
    ):
        pass

    @abstractmethod
    async def get_collection_info(
        self,
        collection_name: str
    ):
        pass
