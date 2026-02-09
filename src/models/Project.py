from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import UploadFile
import pypdf
from ..controllers.BaseController import BaseController
from typing import List


class ProjectSplitters:
    """
    Class to handle file reading and recursive text splitting into chunks.
    Supports PDF and TXT files.
    """

    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 50):
        self.chunk_size: int = chunk_size
        self.chunk_overlap: int = chunk_overlap
        self.chunks: List[str] = []
        self.text: str = ""
        self.splitter: RecursiveCharacterTextSplitter | None = None

    async def initialize_splitter(self) -> None:
        """
        Initialize the LangChain RecursiveCharacterTextSplitter.
        """
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    async def read_file(self, file: UploadFile) -> str:
        """
        Read the contents of a PDF or TXT file and store as text.
        """
        file_name = str(file.filename)
        ext = BaseController.get_file_extention(file_name).lower()

        if ext == "pdf":
            reader = pypdf.PdfReader(file.file)
            self.text = "\n".join(page.extract_text() or "" for page in reader.pages)

        elif ext == "txt":
            content = await file.read()
            self.text = content.decode("utf-8")

        else:
            raise TypeError(
                f"Unsupported file type '{ext}'. Only PDF and TXT are allowed."
            )

        return self.text

    async def make_splitting(self, text: str | None = None) -> List[str]:
        """
        Split the given text (or previously read text) into chunks.
        """
        if self.splitter is None:
            raise RuntimeError("Splitter not initialized. Call initialize_splitter() first.")

        if text is None:
            text = self.text

        if not text:
            raise ValueError("No text provided for splitting.")

        self.chunks = self.splitter.split_text(text)
        return self.chunks

    async def total_chunk_count(self) -> int:
        """
        Return the total number of chunks.
        """
        return len(self.chunks)

    def create_project_name(self, file_name: str) -> str:
        """
        Generate a project name based on the file name.
        """
        base_name = file_name.rsplit(".", 1)[0]
        return f"{base_name}_project"
