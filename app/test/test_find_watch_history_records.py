"""Файл с модульными тестами поиска по истории просмотра"""
from datetime import datetime
from datetime import timedelta
from unittest import main

from app.constants import FileExtension
from app.constants import PROJECT_CONSTANTS
from app.orm_db_actions import add_docmetadata
from app.orm_db_actions import add_watch_history_record
from app.orm_db_actions import get_all_watch_history_records
from app.orm_db_actions import get_watch_history_records_by_name
from app.test.common_settings_for_test_case import CommonSettingsForTestCase


class FindWatchHistoryRecordsTestCase(CommonSettingsForTestCase):
    """Класс модульных тестов поиска по истории просмотра"""

    def test_get_all_watch_history_records(self):
        """Тест поиска всех записей в истории просмотра"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        for i in range(1, PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY + 1):
            add_watch_history_record(
                (datetime.now() + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"), i)
        all_watch_history_records = get_all_watch_history_records()
        self.assertEqual(len(all_watch_history_records),
                         PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY)

    def test_get_watch_history_records_by_name(self):
        """Тест поиска записей в истории просмотра по частичному или полному названию"""
        for i in range(1, 51):
            add_docmetadata(FileExtension.pdf, str(i), str(i))
        for i in range(1, PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY + 1):
            add_watch_history_record(
                (datetime.now() + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"), i)
        watch_history_records = get_watch_history_records_by_name('1')
        self.assertEqual(len(watch_history_records), 14)


if __name__ == '__main__':
    main()
