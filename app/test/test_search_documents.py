"""Файл с модульными тестами поиска по метаданным документа"""
from unittest import main

from app import DB
from app.constants import FileExtension
from app.models import DocMetadata
from app.orm_db_actions import add_docmetadata
from app.orm_db_actions import search_document_by_path
from app.orm_db_actions import search_first_four_documents
from app.orm_db_actions import search_first_four_documents_by_partial_name
from app.orm_db_actions import search_six_documents_by_partial_name_from_number
from app.orm_db_actions import search_six_documents_from_number
from app.test.common_settings_for_test_case import CommonSettingsForTestCase


class SearchDocumentsTestCase(CommonSettingsForTestCase):
    """Класс модульных тестов поиска по метаданным документа"""

    def test_search_document_by_path(self):
        """Тест поиска документа по его полному названию"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        document = search_document_by_path('1')
        document_expected = DB.session.query(DocMetadata) \
            .filter_by(path='1') \
            .first()
        self.assertEqual(document, document_expected)

    def test_search_documents_by_partial_name_from_number(self):
        """Тест поиска документа по его частичному названию"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        documents = search_six_documents_by_partial_name_from_number('4', 2)
        self.assertEqual(len(documents), 1)

    def test_search_six_documents_from_number(self):
        """Тест поиска шести первых документов, начиная с конкретного номера"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        six_documents = search_six_documents_from_number(2)
        self.assertEqual(len(six_documents), 6)

    def test_search_first_four_documents(self):
        """Тест поиска первых 4 документов"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        first_four_documents = search_first_four_documents()
        self.assertEqual(len(first_four_documents), 4)

    def test_search_first_four_documents_by_partial_name(self):
        """Тест поиска первых 4 документов по поисковому запросу"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        first_four_documents = search_first_four_documents_by_partial_name('1')
        self.assertEqual(len(first_four_documents), 4)


if __name__ == '__main__':
    main()
