from fastapi import UploadFile
import pypdf
from typing import List, Optional
from ..servicies.embedding import cohereProvider , geminiProvider
from ..helpers import get_settings
from langchain_text_splitters import RecursiveCharacterTextSplitter




class DataChunk:
    def __init__(self):
        self.content = None
        self.project_id = None
        self.embedding = None
        app = get_settings
        embedding_porvider=app.EMBEDDING_PROVIDER
        
        if embedding_porvider == 'cohere':
            coher_api = app.COHERE_KEY
            self.embed_client = cohereProvider(api_key=coher_api)
            self.embed_client.connect()
        elif embedding_porvider == "gemmni":
            gemmni_key=app.GEMMNI_KEY
            self.embed_client= geminiProvider(api_key=gemmni_key)
            self.embed_client.connect()

    def data_chunk_data(self, content: str, project_id: int, embedding: List[float]):
        self.content = content
        self.project_id = project_id
        self.embedding = embedding
        return self

    def make_chunk_embedding(self, text: str) -> List[float]:
        if not self.embed_client:
            raise RuntimeError("Cohere Client not connected.")
        if not text:
            raise ValueError("Text not provided.")
        
        
        response = self.embed_client.embed_text(text)
        # print(type(response)) # the type is List
        # print(response)
        embedding_vector = response[0].values
        # print("Response of the gemmeni Emmbedding-> ", embedding_vector)

        return embedding_vector
