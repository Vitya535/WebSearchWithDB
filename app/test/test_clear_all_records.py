"""Модульные тесты полной очистки записей в истории просмотра и поиска"""
from datetime import datetime
from unittest import main

from app import DB
from app.constants import PROJECT_CONSTANTS
from app.models import SearchHistoryRecord
from app.models import WatchHistoryRecord
from app.orm_db_actions import add_search_history_record
from app.orm_db_actions import add_watch_history_record
from app.orm_db_actions import clear_all_in_search_history
from app.orm_db_actions import clear_all_in_watch_history
from app.test.common_settings_for_test_case import CommonSettingsForTestCase


class ClearAllRecordsTestCase(CommonSettingsForTestCase):
    """Класс модульных тестов полной очистки записей в истории просмотра и поиска"""

    def test_clear_all_watch_history_records(self):
        """Модульный тест очистки всех записей в истории просмотра"""
        for i in range(1, PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY + 1):
            add_watch_history_record(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), i)
        clear_all_in_watch_history()
        watch_history_records_count = DB.session.query(WatchHistoryRecord).count()
        self.assertEqual(watch_history_records_count, 0)

    def test_clear_all_search_history_records(self):
        """Модульный тест очистки всех записей в истории поиска"""
        for i in range(1, PROJECT_CONSTANTS.RECORDS_COUNT_SEARCH_HISTORY + 1):
            add_search_history_record(str(i), datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        clear_all_in_search_history()
        search_history_records_count = DB.session.query(SearchHistoryRecord).count()
        self.assertEqual(search_history_records_count, 0)


if __name__ == '__main__':
    main()
