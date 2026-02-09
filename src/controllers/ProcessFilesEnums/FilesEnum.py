from enum import Enum

class AllowedFile(Enum):
    TXT="txt"
    PDF="pdf"
    

class FileProccessedEnums(Enum):
    FILE_UPLOAD_SUCCESS="File Upload Success. "
    FILE_UPLOAD_fILED="File Upload Fiiled. "    