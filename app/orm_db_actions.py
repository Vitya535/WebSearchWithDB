"""Файл с запросами к БД"""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy import select

from app import DB
from app import LOG
from app.constants import RECORDS_COUNT_SEARCH_HISTORY
from app.constants import RECORDS_COUNT_WATCH_HISTORY
from app.models import DocMetadata
from app.models import SearchHistoryRecord
from app.models import WatchHistoryRecord
from app.utils import convert_document_list_to_map
from app.utils import divide_watch_history_records_by_datetime
from app.utils import update_datetime_in_search_history_records


def check_count_of_watch_history_records(function_to_decorate):
    """Проверка количества записей в истории просмотра"""
    LOG.debug(f"Enter the check_count_of_watch_history_records with decorated function={function_to_decorate.__name__}")

    def wrapper(search_time: str, doc_id: int):
        LOG.debug(f"Enter the wrapper with search_time={search_time} and doc_id={doc_id}")
        function_to_decorate(search_time, doc_id)
        all_watch_history_records_count = DB.session.query(WatchHistoryRecord) \
            .count()
        LOG.debug(f"All founded watch_history_records is {all_watch_history_records_count}")
        if all_watch_history_records_count > RECORDS_COUNT_WATCH_HISTORY:
            LOG.debug(f"Founded watch_history_records more than limit={RECORDS_COUNT_WATCH_HISTORY}")
            delete_old_watch_history_record()

    return wrapper


def check_count_of_search_history_records(function_to_decorate):
    """Проверка количества записей в истории поиска"""
    LOG.debug(f"Enter the check_count_of_search_history_records with decorated"
              f" function={function_to_decorate.__name__}")

    def wrapper(search_query: str, search_time: str):
        LOG.debug(f"Enter the wrapper with search_query={search_query} and search_time={search_time}")
        function_to_decorate(search_query, search_time)
        all_search_history_records_count = DB.session.query(SearchHistoryRecord) \
            .count()
        LOG.debug(f"All founded search_history_records is {all_search_history_records_count}")
        if all_search_history_records_count > RECORDS_COUNT_SEARCH_HISTORY:
            LOG.debug(f"Founded search_history_records more than limit={RECORDS_COUNT_SEARCH_HISTORY}")
            delete_old_search_history_record()

    return wrapper


def check_on_uniqueness_new_search_history_record(function_to_decorate):
    """Проверка новой записи истории поиска на уникальность, если не уникальна, то обновляем дату"""
    LOG.debug(f"Enter the check_on_uniqueness_new_search_history_record with decorated"
              f" function={function_to_decorate.__name__}")

    def wrapper(search_query: str, search_time: str):
        LOG.debug(f"Enter the wrapper with search_query={search_query} and search_time={search_time}")
        count_of_records_with_search_query = DB.session.query(SearchHistoryRecord) \
            .filter_by(search_query=search_query) \
            .count()
        LOG.debug(f"Count of records with search_query={search_query} is {count_of_records_with_search_query}")
        if count_of_records_with_search_query == 1:
            LOG.debug(f"Record with search_query={search_query} isn't unique. Updating search_time")
            search_history_record = DB.session.query(SearchHistoryRecord) \
                .filter_by(search_query=search_query) \
                .one()
            LOG.debug(f"The search_history_record to update is {search_history_record}")
            search_history_record.search_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            DB.session.flush()
            DB.session.commit()
        else:
            LOG.debug(f"Record with search_query={search_query} is unique. Adding it to database")
            function_to_decorate(search_query, search_time)

    return wrapper


def check_on_uniqueness_new_watch_history_record(function_to_decorate):
    """Проверка новой записи истории просмотров на уникальность, если не уникальна, то обновляем дату"""
    LOG.debug(f"Enter the check_on_uniqueness_new_watch_history_record with decorated"
              f" function={function_to_decorate.__name__}")

    def wrapper(search_time: str, doc_id: int):
        LOG.debug(f"Enter the wrapper with search_time={search_time} and doc_id={doc_id}")
        count_of_records_with_doc_id = DB.session.query(WatchHistoryRecord) \
            .filter_by(doc_id=doc_id) \
            .count()
        LOG.debug(f"Count of records with doc_id={doc_id} is {count_of_records_with_doc_id}")
        if count_of_records_with_doc_id == 1:
            LOG.debug(f"Record with doc_id={doc_id} isn't unique. Updating watch_time")
            watch_history_record = DB.session.query(WatchHistoryRecord) \
                .filter_by(doc_id=doc_id) \
                .one()
            LOG.debug(f"The watch_history_record to update is {watch_history_record}")
            watch_history_record.watch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            DB.session.flush()
            DB.session.commit()
        else:
            LOG.debug(f"Record with doc_id={doc_id} is unique. Adding it to database")
            function_to_decorate(search_time, doc_id)

    return wrapper


def clear_all_in_search_history():
    """Удаление всех записей из истории поиска"""
    LOG.debug(f"Enter the clear_all_in_search_history")
    DB.session.query(SearchHistoryRecord).delete()
    DB.session.flush()
    DB.session.commit()


def clear_all_in_watch_history():
    """Удаление всех записей из истории просмотра"""
    LOG.debug(f"Enter the clear_all_in_watch_history")
    DB.session.query(WatchHistoryRecord).delete()
    DB.session.flush()
    DB.session.commit()


@check_count_of_watch_history_records
@check_on_uniqueness_new_watch_history_record
def add_watch_history_record(search_time: str, doc_id: int):
    """Добавление записи в историю просмотра"""
    LOG.debug(f"Enter the add_watch_history_record with search_time={search_time} and doc_id={doc_id}")
    new_watch_history_record = WatchHistoryRecord(search_time, doc_id)
    LOG.debug(f"A new_watch_history_record for adding is {new_watch_history_record}")
    DB.session.add(new_watch_history_record)
    DB.session.commit()


@check_count_of_search_history_records
@check_on_uniqueness_new_search_history_record
def add_search_history_record(search_query: str, search_time: str):
    """Добавление записи в историю поиска"""
    LOG.debug(f"Enter the add_search_history_record with search_query={search_query} and search_time={search_time}")
    new_search_history_record = SearchHistoryRecord(search_query, search_time)
    LOG.debug(f"A new_search_history_record for adding is {new_search_history_record}")
    DB.session.add(new_search_history_record)
    DB.session.commit()


def delete_old_watch_history_record():
    """Удаление самой старой записи в истории просмотра по дате"""
    LOG.debug(f"Enter the delete_old_watch_history_record")
    watch_history_record_for_delete = DB.session.query(WatchHistoryRecord) \
        .filter(WatchHistoryRecord.watch_time == select([func.min(WatchHistoryRecord.watch_time)])) \
        .first()
    DB.session.query(WatchHistoryRecord) \
        .filter(WatchHistoryRecord.id == watch_history_record_for_delete.id) \
        .delete()
    DB.session.flush()
    DB.session.commit()


def delete_old_search_history_record():
    """Удаление самой старой записи в истории поиска по дате"""
    LOG.debug(f"Enter the delete_old_search_history_record")
    search_history_record_for_delete = DB.session.query(SearchHistoryRecord) \
        .filter(SearchHistoryRecord.search_time == select([func.min(SearchHistoryRecord.search_time)])) \
        .first()
    DB.session.query(SearchHistoryRecord) \
        .filter(SearchHistoryRecord.id == search_history_record_for_delete.id) \
        .delete()
    DB.session.flush()
    DB.session.commit()


def delete_watch_history_record_by_watch_time(watch_time: str):
    """Удаление записи из истории просмотра"""
    LOG.debug(f"Enter the delete_watch_history_record_by_watch_time with watch_time={watch_time}")
    watch_history_record_for_delete = DB.session.query(WatchHistoryRecord) \
        .filter_by(watch_time=watch_time) \
        .first()
    DB.session.query(WatchHistoryRecord) \
        .filter(WatchHistoryRecord.id == watch_history_record_for_delete.id) \
        .delete()
    DB.session.flush()
    DB.session.commit()


def delete_search_history_record_by_search_query(search_query: str):
    """Удаление записи из истории поиска"""
    LOG.debug(f"Enter the delete_search_history_record_by_search_query with search_query={search_query}")
    DB.session.query(SearchHistoryRecord) \
        .filter_by(search_query=search_query) \
        .delete()
    DB.session.flush()
    DB.session.commit()


def search_all_documents():
    """Поиск всех документов в БД"""
    LOG.debug(f"Enter the search_all_documents")
    all_documents = DB.session.query(DocMetadata) \
        .all()
    LOG.debug(f"All documents is {all_documents}")
    return convert_document_list_to_map(all_documents)


def search_document_by_full_name(doc_name: str):
    """Поиск документов в БД по его полному названию"""
    LOG.debug(f"Enter the search_document_by_full_name with doc_name={doc_name}")
    document = DB.session.query(DocMetadata) \
        .filter_by(doc_name=doc_name) \
        .one()
    LOG.debug(f"Document with doc_name={doc_name} is {document}")
    return document


def search_documents_by_partial_name(doc_name: str):
    """Поиск документов в БД по его частичному названию"""
    LOG.debug(f"Enter the search_documents_by_partial_name with doc_name={doc_name}")
    documents = DB.session.query(DocMetadata) \
        .filter(DocMetadata.doc_name.contains(doc_name)) \
        .all()
    LOG.debug(f"Documents with doc_name={doc_name} is {documents}")
    return convert_document_list_to_map(documents)


def get_all_search_history_records():
    """Получение всех записей из истории поиска"""
    LOG.debug(f"Enter the get_all_search_history_records")
    all_search_history_records = DB.session.query(SearchHistoryRecord) \
        .order_by(SearchHistoryRecord.search_time.desc()) \
        .all()
    LOG.debug(f"All founded search_history_records is {all_search_history_records}")
    updated_search_history_records = \
        update_datetime_in_search_history_records(all_search_history_records)
    return updated_search_history_records


def get_all_watch_history_records():
    """Получение всех записей из истории просмотра"""
    LOG.debug(f"Enter the get_all_watch_history_records")
    all_watch_history_records = DB.session.query(WatchHistoryRecord, DocMetadata) \
        .filter(WatchHistoryRecord.doc_id == DocMetadata.id) \
        .order_by(WatchHistoryRecord.watch_time.desc()) \
        .all()
    LOG.debug(f"All founded watch_history_records is {all_watch_history_records}")
    watch_history_records_today, watch_history_records_yesterday, watch_history_records_days_ago = \
        divide_watch_history_records_by_datetime(all_watch_history_records)
    return watch_history_records_today, watch_history_records_yesterday, watch_history_records_days_ago


def get_watch_history_records_by_name(doc_name: str):
    """Получение записей из истории просмотра по названию документа"""
    LOG.debug(f"Enter the get_watch_history_records_by_name with doc_name={doc_name}")
    watch_history_records = DB.session.query(WatchHistoryRecord, DocMetadata) \
        .filter(WatchHistoryRecord.doc_id == DocMetadata.id) \
        .filter(DocMetadata.doc_name.contains(doc_name)) \
        .order_by(WatchHistoryRecord.watch_time.desc()) \
        .all()
    LOG.debug(f"All watch_history_records founded by doc_name={doc_name} is {watch_history_records}")
    watch_history_records_today, watch_history_records_yesterday, watch_history_records_days_ago = \
        divide_watch_history_records_by_datetime(watch_history_records)
    return watch_history_records_today, watch_history_records_yesterday, watch_history_records_days_ago


def get_search_history_records_by_name(search_query: str):
    """Получение записей из истории поиска по названию"""
    LOG.debug(f"Enter the get_all_search_history_records_by_name with search_query={search_query}")
    search_history_records = DB.session.query(SearchHistoryRecord) \
        .filter(SearchHistoryRecord.search_query.contains(search_query)) \
        .order_by(SearchHistoryRecord.search_time.desc()) \
        .all()
    LOG.debug(f"All search_history_records founded by search_query={search_query} is {search_history_records}")
    updated_search_history_records = \
        update_datetime_in_search_history_records(search_history_records)
    return updated_search_history_records
