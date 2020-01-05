"""Тест добавления записи в историю просмотра"""
from datetime import datetime
from datetime import timedelta
from unittest import main

from sqlalchemy import func
from sqlalchemy import select

from app import DB
from app.constants import PROJECT_CONSTANTS
from app.models import WatchHistoryRecord
from app.orm_db_actions import add_watch_history_record
from app.test.common_settings_for_test_case import CommonSettingsForTestCase


class AddWatchHistoryRecordTestCase(CommonSettingsForTestCase):
    """Модульные тесты добавления записи в историю просмотра"""

    def test_add_watch_history_record(self):
        """Тест обычного добавления записи в историю просмотра"""
        add_watch_history_record("2017-11-18 14:25:00", 1)
        count_of_watch_history_records = DB.session.query(WatchHistoryRecord).count()
        self.assertEqual(count_of_watch_history_records, 1)

    def test_check_on_uniqueness_new_watch_history_record(self):
        """Тест добавления неуникальной записи в историю просмотра"""
        add_watch_history_record("2017-11-18 14:25:00", 1)
        add_watch_history_record(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1)
        watch_history_record = DB.session.query(WatchHistoryRecord).one()
        self.assertEqual(watch_history_record.watch_time,
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def test_check_count_of_watch_history_records_with_same_watch_time(self):
        """Тест добавления записи в историю просмотра
        в случае превышения лимита записей при одинаковых датах"""
        for i in range(1, PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY + 1):
            add_watch_history_record(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), i)
        watch_history_record_with_min_watch_time = DB.session.query(WatchHistoryRecord) \
            .filter(WatchHistoryRecord.watch_time ==
                    select([func.min(WatchHistoryRecord.watch_time)])) \
            .first()
        add_watch_history_record(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                 PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY + 1)
        watch_history_record_with_max_watch_time = DB.session.query(WatchHistoryRecord) \
            .filter(WatchHistoryRecord.watch_time ==
                    select([func.max(WatchHistoryRecord.watch_time)])) \
            .first()
        watch_history_records = DB.session.query(WatchHistoryRecord).all()
        self.assertEqual(len(watch_history_records), PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY)
        self.assertIn(watch_history_record_with_max_watch_time, watch_history_records)
        self.assertNotIn(watch_history_record_with_min_watch_time, watch_history_records)

    def test_check_count_of_watch_history_records_with_different_watch_time(self):
        """Тест добавления записи в историю просмотра
        в случае превышения лимита записей при разных датах"""
        for i in range(1, PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY + 1):
            add_watch_history_record(
                (datetime.now() + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S"), i)
        watch_history_record_with_min_watch_time = DB.session.query(WatchHistoryRecord) \
            .filter(WatchHistoryRecord.watch_time ==
                    select([func.min(WatchHistoryRecord.watch_time)])) \
            .first()
        add_watch_history_record((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                                 PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY + 1)
        watch_history_record_with_max_watch_time = DB.session.query(WatchHistoryRecord) \
            .filter(WatchHistoryRecord.watch_time ==
                    select([func.max(WatchHistoryRecord.watch_time)])) \
            .first()
        watch_history_records = DB.session.query(WatchHistoryRecord).all()
        self.assertEqual(len(watch_history_records), PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY)
        self.assertIn(watch_history_record_with_max_watch_time, watch_history_records)
        self.assertNotIn(watch_history_record_with_min_watch_time, watch_history_records)


if __name__ == '__main__':
    main()
