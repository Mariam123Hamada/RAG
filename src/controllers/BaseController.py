from fastapi import HTTPException
from .ProcessFilesEnums.FilesEnum import AllowedFile


class BaseController:

    @staticmethod
    def get_file_extension(filename: str) -> str:
        if "." not in filename:
            raise HTTPException(
                status_code=400,
                detail="File must have an extension"
            )

        ext = filename.rsplit(".", 1)[-1].lower()

        if ext not in {
            AllowedFile.PDF.value,
            AllowedFile.TXT.value
        }:
            raise HTTPException(
                status_code=400,
                detail="Only PDF and TXT files are allowed"
            )

        return ext
