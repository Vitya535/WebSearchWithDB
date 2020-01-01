"""Файл с модульными тестами поиска записей в истории поиска"""
from datetime import datetime
from datetime import timedelta
from unittest import main

from app.constants import ProjectConstants
from app.orm_db_actions import add_search_history_record
from app.orm_db_actions import get_all_search_history_records
from app.orm_db_actions import get_search_history_records_by_name
from .common_settings_for_test_case import CommonSettingsForTestCase


class FindSearchHistoryRecordsTestCase(CommonSettingsForTestCase):
    """Класс модульных тестов поиска записей в истории поиска"""

    def test_get_all_search_history_records(self):
        """Тест поиска всех записей в истории поиска"""
        for i in range(1, ProjectConstants.RECORDS_COUNT_SEARCH_HISTORY + 1):
            add_search_history_record(str(i), (datetime.now() + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"))
        all_search_history_records = get_all_search_history_records()
        self.assertEqual(len(all_search_history_records), ProjectConstants.RECORDS_COUNT_SEARCH_HISTORY)

    def test_get_search_history_records_by_name(self):
        """Тест поиска всех записей в истории поиска по частичному или полному поисковому запросу"""
        for i in range(1, ProjectConstants.RECORDS_COUNT_SEARCH_HISTORY + 1):
            add_search_history_record(str(i), (datetime.now() + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"))
        search_history_records = get_search_history_records_by_name('1')
        self.assertEqual(len(search_history_records), 14)


if __name__ == '__main__':
    main()
