"""Файл с различными вспомогательными классами и методами"""
from datetime import datetime
from enum import Enum
from math import ceil

from app import LOG
from app.constants import COUNT_OF_DOCS_IN_ROW


class FileExtension(str, Enum):
    """Класс со списком текстовых файловых расширений"""
    pdf = 'pdf'
    doc = 'doc'
    docx = 'docx'
    txt = 'txt'


def convert_document_list_to_map(documents: list):
    """Конвертирование списка документов в словарь"""
    LOG.debug(f"Enter the convert_document_list_to_map with documents={documents}")
    count_of_rows = ceil(len(documents) / COUNT_OF_DOCS_IN_ROW)
    LOG.debug(f"Count of rows in map: {count_of_rows}")
    all_documents_map = \
        {i: documents[i * count_of_rows:i * count_of_rows + 3] for i in range(count_of_rows)}
    LOG.debug(f"The created map from docs is {all_documents_map}")
    return all_documents_map


def update_datetime_in_search_history_records(search_history_records: list):
    """Приведение времени в истории поиска к более красивому виду"""
    LOG.debug(f"Enter the update_datetime_in_search_history_records with "
              f"search_history_records={search_history_records}")
    for record in search_history_records:
        time_diff = datetime.now() - datetime.strptime(record.search_time, "%Y-%m-%d %H:%M:%S")
        time_diff_hours = time_diff.total_seconds() / 3600
        if time_diff_hours < 24:
            record.search_time = 'Сегодня'
        elif 24 <= time_diff_hours <= 48:
            record.search_time = 'Вчера'
        else:
            record.search_time = 'Несколько дней назад'
    LOG.debug(f"Search_history_records with updated datetime is {search_history_records}")
    return search_history_records


def divide_watch_history_records_by_datetime(watch_history_records: list):
    """Разделение одного списка истории просмотров на три по времени"""
    LOG.debug(f"Enter the divide_watch_history_records_by_datetime with watch_history_records={watch_history_records}")
    watch_history_records_today = list()
    watch_history_records_yesterday = list()
    watch_history_records_days_ago = list()
    for record in watch_history_records:
        time_diff = datetime.now() - datetime.strptime(record[0].watch_time, "%Y-%m-%d %H:%M:%S")
        time_diff_hours = time_diff.total_seconds() / 3600
        if time_diff_hours < 24:
            watch_history_records_today.append(record)
        elif 24 <= time_diff_hours <= 48:
            watch_history_records_yesterday.append(record)
        else:
            watch_history_records_days_ago.append(record)
    LOG.debug(f"Records for today is {watch_history_records_today},"
              f" for yesterday is {watch_history_records_yesterday},"
              f" days ago is {watch_history_records_days_ago}")
    return watch_history_records_today, watch_history_records_yesterday, watch_history_records_days_ago
