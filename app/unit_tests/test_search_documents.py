"""Файл с модульными тестами поиска по метаданным документа"""
from unittest import main

from app import DB
from app.models import DocMetadata
from app.orm_db_actions import add_docmetadata
from app.orm_db_actions import search_all_documents
from app.orm_db_actions import search_document_by_full_name
from app.orm_db_actions import search_documents_by_partial_name
from app.utils import FileExtension
from .common_settings_for_test_case import CommonSettingsForTestCase


class SearchDocumentsTestCase(CommonSettingsForTestCase):
    """Класс модульных тестов поиска по метаданным документа"""

    def test_search_all_documents(self):
        """Тест поиска всех документов"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        all_documents = search_all_documents()
        self.assertEqual(len(all_documents), 50)

    def test_search_document_by_full_name(self):
        """Тест поиска документа по его полному названию"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        document = search_document_by_full_name('1')
        document_expected = DB.session.query(DocMetadata) \
            .filter_by(doc_name='1') \
            .one()
        self.assertEqual(document, document_expected)

    def test_search_documents_by_partial_name(self):
        """Тест поиска документа по его частичному названию"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        documents = search_documents_by_partial_name('4')
        self.assertEqual(len(documents), 14)


if __name__ == '__main__':
    main()
