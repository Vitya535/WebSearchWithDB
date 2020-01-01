"""Модульные тесты удаления записей по определенным параметрам из истории поиска и просмотра"""
from datetime import datetime
from unittest import main

from app import DB
from app.constants import ProjectConstants
from app.models import SearchHistoryRecord
from app.models import WatchHistoryRecord
from app.orm_db_actions import add_search_history_record
from app.orm_db_actions import add_watch_history_record
from app.orm_db_actions import delete_search_history_record_by_search_query
from app.orm_db_actions import delete_watch_history_record_by_doc_name
from .common_settings_for_test_case import CommonSettingsForTestCase
from app.utils import FileExtension
from app.orm_db_actions import add_docmetadata


class DeleteRecordByFieldValueTestCase(CommonSettingsForTestCase):
    """Класс модульных тестов удаления записей по определенным параметрам из истории поиска и просмотра"""

    def test_delete_watch_history_record_by_doc_name(self):
        """Модульный тест удаления записи из истории просмотра по дате просмотра"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        for i in range(1, ProjectConstants.RECORDS_COUNT_WATCH_HISTORY + 1):
            add_watch_history_record(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), i)
        watch_history_record_for_delete = DB.session.query(WatchHistoryRecord) \
            .filter_by(doc_id=1) \
            .first()
        delete_watch_history_record_by_doc_name('1')
        watch_history_records = DB.session.query(WatchHistoryRecord).all()
        self.assertEqual(len(watch_history_records), ProjectConstants.RECORDS_COUNT_WATCH_HISTORY - 1)
        self.assertNotIn(watch_history_record_for_delete, watch_history_records)

    def test_delete_search_history_record_by_search_query(self):
        """Модульный тест удаления записи из истории поиска по поисковому запросу"""
        for i in range(1, ProjectConstants.RECORDS_COUNT_SEARCH_HISTORY + 1):
            add_search_history_record(str(i), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        search_history_record_for_delete = DB.session.query(SearchHistoryRecord) \
            .filter_by(search_query="50") \
            .first()
        delete_search_history_record_by_search_query("50")
        search_history_records = DB.session.query(SearchHistoryRecord).all()
        self.assertEqual(len(search_history_records), ProjectConstants.RECORDS_COUNT_SEARCH_HISTORY - 1)
        self.assertNotIn(search_history_record_for_delete, search_history_records)


if __name__ == '__main__':
    main()
