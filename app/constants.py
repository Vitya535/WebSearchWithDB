"""Файл, содержащий в себе разлчиные константы для проекта"""

from collections import namedtuple
from enum import Enum


class FileExtension(str, Enum):
    """Класс со списком текстовых файловых расширений"""
    pdf = 'pdf'
    docx = 'docx'
    odt = 'odt'
    ods = 'ods'


ProjectConstants = namedtuple('ProjectConstants',
                              'COUNT_OF_DOCS_IN_ROW '
                              'RECORDS_COUNT_WATCH_HISTORY '
                              'RECORDS_COUNT_SEARCH_HISTORY '
                              'DOCS_COUNT_FOR_UPLOAD')
PROJECT_CONSTANTS = ProjectConstants(2, 50, 50, 6)
