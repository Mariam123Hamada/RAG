from fastapi import UploadFile
import pypdf
from typing import List, Optional
from ..servicies.embedding import cohereProvider
from ..helpers import get_settings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .DataChunk import DataChunk



class ProjectSplitters:
    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chunks: List[str] = []
        self.text: str = ""
        self.splitter: Optional[RecursiveCharacterTextSplitter] = None
        self.project_name: str = ""

    async def initialize_splitter(self) -> None:
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    async def read_file(self, file: UploadFile) -> str:
        file_name = str(file.filename)
        self.project_name = self.create_project_name(file_name)
        ext = file_name.split(".")[-1].lower()

        if ext == "pdf":
            reader = pypdf.PdfReader(file.file)
            self.text = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif ext == "txt":
            content = await file.read()
            self.text = content.decode("utf-8")
        else:
            raise TypeError(f"Unsupported file type '{ext}'.")

        return self.text

    async def make_splitting(self, text: Optional[str] = None) -> List[str]:
        if self.splitter is None:
            await self.initialize_splitter()

        target_text = text if text is not None else self.text

        if not target_text:
            raise ValueError("No text provided for splitting.")

        self.chunks = self.splitter.split_text(target_text)
        return self.chunks

    async def make_DataChunk_Split(self, chunks: List[str], project_id: int) -> List[DataChunk]:
        if not chunks:
            raise ValueError("No chunks provided.")

        data_chunks: List[DataChunk] = []

        for chunk in chunks:
            data_chunk = DataChunk()
            embedding = data_chunk.make_chunk_embedding(chunk)
            data_chunk.data_chunk_data(
                content=chunk,
                project_id=project_id,
                embedding=embedding
            )
            data_chunks.append(data_chunk)

        return data_chunks

    async def total_chunk_count(self) -> int:
        return len(self.chunks)

    def create_project_name(self, file_name: str) -> str:
        base_name = file_name.rsplit(".", 1)[0]
        return f"{base_name}_project"
