from fastapi import HTTPException
from .ProcessFilesEnums.FilesEnum import AllowedFile


class BaseController:

    @staticmethod
    def get_file_extension(filename: str) -> str:
        ext = filename.split(".")[-1].lower()

        if ext not in (
            AllowedFile.PDF.value,
            AllowedFile.TXT.value
        ):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and TXT files are allowed"
            )

        return ext
