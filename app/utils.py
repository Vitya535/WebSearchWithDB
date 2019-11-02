"""Файл с различными вспомогательными классами и методами"""
from enum import Enum


class FileExtension(str, Enum):
    """Класс со списком текстовых файловых расширений"""
    PDF = 'pdf'
    DOC = 'doc'
    DOCX = 'docx'
    TXT = 'txt'
