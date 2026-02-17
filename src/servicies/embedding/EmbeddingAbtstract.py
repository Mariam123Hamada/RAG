from typing import List
from abc import ABC ,abstractmethod

class EmbeddingAbstract(ABC):
    def __init__(self, api_key: str):
        self.co = None
        self.api_key = api_key
    
    @abstractmethod
    def connect(self):
        pass 

    @abstractmethod
    def embed_text(self, input_text: str):
        pass 
    @abstractmethod
    def extrect_embed(self, response):
        pass 
    
    @abstractmethod
    def prepare_text(self, text: str):
        pass 
    @abstractmethod
    def disconnect(self):
        pass 
