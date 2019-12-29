"""Тест добавления записи в историю поиска"""
from datetime import datetime
from datetime import timedelta
from unittest import main

from sqlalchemy import func
from sqlalchemy import select

from app import DB
from app.constants import RECORDS_COUNT_SEARCH_HISTORY
from app.models import SearchHistoryRecord
from app.orm_db_actions import add_search_history_record
from .common_settings_for_test_case import CommonSettingsForTestCase


class AddSearchHistoryRecordTestCase(CommonSettingsForTestCase):
    """Модульные тесты добавления записи в историю поиска"""

    def test_add_search_history_record(self):
        """Тест обычного добавления записи в историю поиска"""
        add_search_history_record("Bo", "2017-11-18 14:25:00")
        count_of_search_history_records = DB.session.query(SearchHistoryRecord).count()
        self.assertEqual(count_of_search_history_records, 1)

    def test_check_on_uniqueness_new_search_history_record(self):
        """Тест добавления неуникальной записи в историю поиска"""
        add_search_history_record("Bo", "2017-11-18 14:25:00")
        add_search_history_record("Bo", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        search_history_record = DB.session.query(SearchHistoryRecord).one()
        self.assertEqual(search_history_record.search_time,
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def test_check_count_of_search_history_records_with_same_search_time(self):
        """Тест добавления записи в историю поиска в случае превышения лимита записей при одинаковых датах"""
        for i in range(1, RECORDS_COUNT_SEARCH_HISTORY + 1):
            add_search_history_record(str(i), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        search_history_record_with_min_search_time = DB.session.query(SearchHistoryRecord) \
            .filter(SearchHistoryRecord.search_time == select([func.min(SearchHistoryRecord.search_time)])) \
            .first()
        add_search_history_record(str(RECORDS_COUNT_SEARCH_HISTORY + 1), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        search_history_record_with_max_search_time = DB.session.query(SearchHistoryRecord) \
            .filter(SearchHistoryRecord.search_time == select([func.max(SearchHistoryRecord.search_time)])) \
            .first()
        search_history_records = DB.session.query(SearchHistoryRecord).all()
        self.assertEqual(len(search_history_records), RECORDS_COUNT_SEARCH_HISTORY)
        self.assertIn(search_history_record_with_max_search_time, search_history_records)
        self.assertNotIn(search_history_record_with_min_search_time, search_history_records)

    def test_check_count_of_search_history_records_with_different_search_time(self):
        """Тест добавления записи в историю поиска в случае превышения лимита записей при разных датах"""
        for i in range(1, RECORDS_COUNT_SEARCH_HISTORY + 1):
            add_search_history_record(str(i), (datetime.now() + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"))
        search_history_record_with_min_search_time = DB.session.query(SearchHistoryRecord) \
            .filter(SearchHistoryRecord.search_time == select([func.min(SearchHistoryRecord.search_time)])) \
            .first()
        add_search_history_record(str(RECORDS_COUNT_SEARCH_HISTORY + 1),
                                  (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
        search_history_record_with_max_search_time = DB.session.query(SearchHistoryRecord) \
            .filter(SearchHistoryRecord.search_time == select([func.max(SearchHistoryRecord.search_time)])) \
            .first()
        search_history_records = DB.session.query(SearchHistoryRecord).all()
        self.assertEqual(len(search_history_records), RECORDS_COUNT_SEARCH_HISTORY)
        self.assertIn(search_history_record_with_max_search_time, search_history_records)
        self.assertNotIn(search_history_record_with_min_search_time, search_history_records)


if __name__ == '__main__':
    main()
