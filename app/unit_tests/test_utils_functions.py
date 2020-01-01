"""Файл с модульными тестами вспомогательных функций"""
from datetime import datetime
from datetime import timedelta
from math import ceil
from unittest import main

from app import DB
from app.constants import ProjectConstants
from app.models import DocMetadata
from app.models import SearchHistoryRecord
from app.models import WatchHistoryRecord
from app.orm_db_actions import add_docmetadata
from app.orm_db_actions import add_search_history_record
from app.orm_db_actions import add_watch_history_record
from app.utils import FileExtension
from app.utils import convert_document_list_to_map
from app.utils import divide_watch_history_records_by_datetime
from app.utils import update_datetime_in_search_history_records
from .common_settings_for_test_case import CommonSettingsForTestCase


class UtilsFunctionsTestCase(CommonSettingsForTestCase):
    """Класс модульных тестов вспомогательных функций"""

    def test_convert_document_list_to_map(self):
        """Тест конвертации списка документов в словарь"""
        for i in range(1, 52):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        documents = DB.session.query(DocMetadata).all()
        documents_map = convert_document_list_to_map(documents)
        for value in documents_map.values():
            self.assertIn(len(value), range(1, ProjectConstants.COUNT_OF_DOCS_IN_ROW + 1))
        count_of_rows = ceil(len(documents) / ProjectConstants.COUNT_OF_DOCS_IN_ROW)
        self.assertEqual(count_of_rows, 26)

    def test_update_datetime_in_search_history_records(self):
        """Тест апдейта даты в списка истории поиска"""
        for i in range(1, ProjectConstants.RECORDS_COUNT_SEARCH_HISTORY + 1):
            add_search_history_record(str(i), (datetime.now() + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"))
        search_history_records = DB.session.query(SearchHistoryRecord).all()
        updated_search_history_records = update_datetime_in_search_history_records(search_history_records)
        for record in updated_search_history_records:
            self.assertIn(record.search_time, list(['Сегодня', 'Вчера', 'Несколько дней назад']))

    def test_divide_watch_history_records_by_datetime(self):
        """Тест разделения одного списка на несколько по дате просмотра"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        for i in range(1, ProjectConstants.RECORDS_COUNT_WATCH_HISTORY + 1):
            add_watch_history_record((datetime.now() + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"), i)
        watch_history_records = DB.session.query(WatchHistoryRecord, DocMetadata) \
            .filter(WatchHistoryRecord.doc_id == DocMetadata.id) \
            .order_by(WatchHistoryRecord.watch_time.desc()) \
            .all()
        watch_history_records_today, watch_history_records_yesterday, watch_history_records_days_ago = \
            divide_watch_history_records_by_datetime(watch_history_records)
        for record in watch_history_records_today:
            self.assertLess(
                (datetime.now() - datetime.strptime(record[0].watch_time, "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600,
                24)
        for record in watch_history_records_yesterday:
            self.assertLessEqual(
                (datetime.now() - datetime.strptime(record[0].watch_time, "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600,
                48)
            self.assertGreaterEqual(
                (datetime.now() - datetime.strptime(record[0].watch_time, "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600,
                24)
        for record in watch_history_records_days_ago:
            self.assertGreater(
                (datetime.now() - datetime.strptime(record[0].watch_time, "%Y-%m-%d %H:%M:%S")).total_seconds() / 3600,
                48)


if __name__ == '__main__':
    main()
