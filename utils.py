from enum import Enum


class FileExtension(str, Enum):
    PDF = 'pdf'
    DOC = 'doc'
    DOCX = 'docx'
    TXT = 'txt'
