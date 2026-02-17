from typing import List
# import google.generativeai as genai
from google import genai
from ..EmbeddingAbtstract import EmbeddingAbstract


class geminiProvider(EmbeddingAbstract):
    def __init__(self, api_key: str):
        self.client = None
        self.api_key = api_key

    def connect(self):
        if not self.api_key:
            raise ValueError("There is No Gemini API Key.")

        # genai.configure(api_key=self.api_key)
        self.client = genai.Client(api_key=self.api_key)

    def embed_text(self, input_text: str):
        """ This MEthods is used to make Embedding for texet and the 
            Style of intlize Client is as defined on the Documentsions."""
        if input_text is None:
            raise RuntimeError("There is No text to embed")

        if self.client is None:
            raise RuntimeError("Gemini client is not connected")

        prepared_text = self.prepare_text(input_text)

        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=prepared_text
        )
        
        # embedding_vector = [vect for vect in response.embeddings] 
        embedding_vector = response.embeddings
        return embedding_vector

    def extrect_embed(self, response):
        return response["embeddings"]

    def prepare_text(self, text: str):
        return text

    def disconnect(self):
        self.client = None
