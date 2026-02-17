from typing import List
import cohere
from ....helpers.config import get_settings
from ..EmbeddingAbtstract import EmbeddingAbstract
from ....helpers import get_settings


class cohereProvider(EmbeddingAbstract):
    def __init__(self, api_key: str):
        self.co = None
        self.api_key = api_key

    def connect(self):
        """Initialize Cohere client"""
        if not self.api_key:
            raise ValueError("There is No Cohere APi Key.")
        self.co = cohere.Client(self.api_key)

    def embed_text(self, input_text: str):
        if input_text is None:
            raise RuntimeError("There is No text to embed")

        if self.co is None:
            raise RuntimeError("Cohere client is not connected")

        prepered_text = self.prepare_text(input_text)

        response = self.co.embed(
            texts=[prepered_text],                 
            model="embed-english-v3.0",            
            input_type="search_document"           
        )

        return response

    def extrect_embed(self, response):
        """Extract embedding vector from response"""
        return response.embeddings[0]

    def prepare_text(self, text: str):
        """
        Prepare text before sending to Cohere.
        (Cohere expects plain string for embed v3 models)
        in other version  there are anthor schem look at the documnets.
        """
        return text
    
    def disconnect(self):
        self.co=None
