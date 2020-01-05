"""Файл с различными вспомогательными классами и методами"""
from datetime import datetime
from math import ceil

from app import LOG
from app.constants import PROJECT_CONSTANTS
from app.models import DOC_METADATA_SCHEMA


def convert_document_list_to_map(documents: list) -> dict:
    """Конвертирование списка документов в словарь"""
    LOG.debug(f"Enter the convert_document_list_to_map with documents={documents}")
    count_of_rows = ceil(len(documents) / PROJECT_CONSTANTS.COUNT_OF_DOCS_IN_ROW)
    LOG.debug(f"Count of rows in map: {count_of_rows}")
    all_documents_map = {
        i: documents[i * PROJECT_CONSTANTS.COUNT_OF_DOCS_IN_ROW:
                     (i + 1) * PROJECT_CONSTANTS.COUNT_OF_DOCS_IN_ROW] for i in
        range(count_of_rows)}
    LOG.debug(f"The created map from docs is {all_documents_map}")
    return all_documents_map


def update_datetime_in_search_history_records(search_history_records: list) -> list:
    """Приведение времени в истории поиска к более красивому виду"""
    LOG.debug(f"Enter the update_datetime_in_search_history_records with "
              f"search_history_records={search_history_records}")
    for record in search_history_records:
        time_diff = datetime.now().date() - \
                    datetime.strptime(record.search_time, "%Y-%m-%d %H:%M:%S").date()
        if time_diff.days < 1:
            record.search_time = 'Сегодня'
        elif 1 <= time_diff.days <= 2:
            record.search_time = 'Вчера'
        else:
            record.search_time = 'Несколько дней назад'
    LOG.debug(f"Search_history_records with updated datetime is {search_history_records}")
    return search_history_records


def divide_watch_history_records_by_datetime(watch_history_records: list) -> dict:
    """Разделение одного списка истории просмотров на три по времени"""
    LOG.debug(f"Enter the divide_watch_history_records_by_datetime "
              f"with watch_history_records={watch_history_records}")

    watch_history_records_today = list(filter(
        lambda record: (datetime.now().date() - datetime.strptime(
            record[0].watch_time, "%Y-%m-%d %H:%M:%S").date()).days < 1,
        watch_history_records))

    watch_history_records_yesterday = list(filter(
        lambda record: 1 <= (datetime.now().date() - datetime.strptime(
            record[0].watch_time, "%Y-%m-%d %H:%M:%S").date()).days <= 2,
        watch_history_records))

    watch_history_records_days_ago = list(filter(
        lambda record: (datetime.now().date() - datetime.strptime(
            record[0].watch_time, "%Y-%m-%d %H:%M:%S").date()).days > 2,
        watch_history_records))

    watch_history_records_dict = {'Сегодня': watch_history_records_today,
                                  'Вчера': watch_history_records_yesterday,
                                  'Несколько дней назад': watch_history_records_days_ago}

    LOG.debug(f"Records for today is {watch_history_records_today},"
              f" for yesterday is {watch_history_records_yesterday},"
              f" days ago is {watch_history_records_days_ago}")
    LOG.debug(f"watch_history_records_dict={watch_history_records_dict}")
    return watch_history_records_dict


def convert_document_map_to_json(document_map: dict) -> dict:
    document_map = {key: DOC_METADATA_SCHEMA.dump(document_map[key]) for key in document_map.keys()}
    return document_map
