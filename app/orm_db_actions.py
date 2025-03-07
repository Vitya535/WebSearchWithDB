"""Файл с запросами к БД"""

from datetime import datetime

from sqlalchemy import and_
from sqlalchemy import between
from sqlalchemy import func

from app import DB
from app import LOG
from app.constants import PROJECT_CONSTANTS
from app.models import DocMetadata
from app.models import SearchHistoryRecord
from app.models import WatchHistoryRecord


def check_count_of_watch_history_records(function_to_decorate):
    """Проверка количества записей в истории просмотра"""
    LOG.debug(f"Enter the check_count_of_watch_history_records "
              f"with decorated function={function_to_decorate.__name__}")

    def wrapper(search_time: str, doc_id: int):
        LOG.debug(f"Enter the wrapper with search_time={search_time} and doc_id={doc_id}")
        function_to_decorate(search_time, doc_id)
        all_watch_history_records_count = DB.session.query(WatchHistoryRecord) \
            .count()
        LOG.debug(f"All founded watch_history_records is {all_watch_history_records_count}")
        if all_watch_history_records_count > PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY:
            LOG.debug(f"Founded watch_history_records "
                      f"more than limit={PROJECT_CONSTANTS.RECORDS_COUNT_WATCH_HISTORY}")
            delete_old_watch_history_record()

    return wrapper


def check_count_of_search_history_records(function_to_decorate):
    """Проверка количества записей в истории поиска"""
    LOG.debug(f"Enter the check_count_of_search_history_records with decorated"
              f" function={function_to_decorate.__name__}")

    def wrapper(search_query: str, search_time: str):
        LOG.debug(f"Enter the wrapper with search_query={search_query} "
                  f"and search_time={search_time}")
        function_to_decorate(search_query, search_time)
        all_search_history_records_count = DB.session.query(SearchHistoryRecord) \
            .count()
        LOG.debug(f"All founded search_history_records is {all_search_history_records_count}")
        if all_search_history_records_count > PROJECT_CONSTANTS.RECORDS_COUNT_SEARCH_HISTORY:
            LOG.debug(f"Founded search_history_records "
                      f"more than limit={PROJECT_CONSTANTS.RECORDS_COUNT_SEARCH_HISTORY}")
            delete_old_search_history_record()

    return wrapper


def check_on_uniqueness_new_search_history_record(function_to_decorate):
    """Проверка новой записи истории поиска на уникальность, если не уникальна, то обновляем дату"""
    LOG.debug(f"Enter the check_on_uniqueness_new_search_history_record with decorated"
              f" function={function_to_decorate.__name__}")

    def wrapper(search_query: str, search_time: str):
        LOG.debug(f"Enter the wrapper with search_query={search_query} "
                  f"and search_time={search_time}")
        search_history_record = DB.session.query(SearchHistoryRecord) \
            .filter_by(search_query=search_query) \
            .first()
        LOG.debug(f"search_history_record={search_history_record}")
        if search_history_record:
            LOG.debug(f"Record with search_query={search_query} isn't unique. Updating search_time")
            LOG.debug(f"The search_history_record to update is {search_history_record}")
            search_history_record.search_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            DB.session.flush()
            DB.session.commit()
        else:
            LOG.debug(f"Record with search_query={search_query} is unique. Adding it to database")
            function_to_decorate(search_query, search_time)

    return wrapper


def check_on_uniqueness_new_watch_history_record(function_to_decorate):
    """Проверка новой записи истории просмотров на уникальность,
     если не уникальна, то обновляем дату"""
    LOG.debug(f"Enter the check_on_uniqueness_new_watch_history_record "
              f"with decorated function={function_to_decorate.__name__}")

    def wrapper(search_time: str, doc_id: int):
        LOG.debug(f"Enter the wrapper with search_time={search_time} and doc_id={doc_id}")
        watch_history_record = DB.session.query(WatchHistoryRecord) \
            .filter_by(doc_id=doc_id) \
            .first()
        LOG.debug(f"watch_history_record={watch_history_record}")
        if watch_history_record:
            LOG.debug(f"Record with doc_id={doc_id} isn't unique. Updating watch_time")
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
    LOG.debug(f"Enter the add_watch_history_record "
              f"with search_time={search_time} and doc_id={doc_id}")
    new_watch_history_record = WatchHistoryRecord(search_time, doc_id)
    LOG.debug(f"A new_watch_history_record for adding is {new_watch_history_record}")
    DB.session.add(new_watch_history_record)
    DB.session.commit()


@check_count_of_search_history_records
@check_on_uniqueness_new_search_history_record
def add_search_history_record(search_query: str, search_time: str):
    """Добавление записи в историю поиска"""
    LOG.debug(f"Enter the add_search_history_record "
              f"with search_query={search_query} and search_time={search_time}")
    new_search_history_record = SearchHistoryRecord(search_query, search_time)
    LOG.debug(f"A new_search_history_record for adding is {new_search_history_record}")
    DB.session.add(new_search_history_record)
    DB.session.commit()


def delete_old_watch_history_record():
    """Удаление самой старой записи в истории просмотра по дате"""
    LOG.debug(f"Enter the delete_old_watch_history_record")
    watch_history_record_for_delete = DB.session.query(
        WatchHistoryRecord.id, func.min(WatchHistoryRecord.watch_time)) \
        .first()
    DB.session.query(WatchHistoryRecord) \
        .filter(WatchHistoryRecord.id == watch_history_record_for_delete.id) \
        .delete()
    DB.session.flush()
    DB.session.commit()


def delete_old_search_history_record():
    """Удаление самой старой записи в истории поиска по дате"""
    LOG.debug(f"Enter the delete_old_search_history_record")
    search_history_record_for_delete = DB.session.query(
        SearchHistoryRecord.id, func.min(SearchHistoryRecord.search_time)) \
        .first()
    DB.session.query(SearchHistoryRecord) \
        .filter(SearchHistoryRecord.id == search_history_record_for_delete.id) \
        .delete()
    DB.session.flush()
    DB.session.commit()


def delete_watch_history_record_by_doc_name(doc_name: str):
    """Удаление записи из истории просмотра по имени документа"""
    LOG.debug(f"Enter the delete_watch_history_record_by_watch_time with doc_name={doc_name}")
    document_id = DB.session.query(DocMetadata.id) \
        .filter_by(doc_name=doc_name) \
        .first().id
    DB.session.query(WatchHistoryRecord) \
        .filter(WatchHistoryRecord.doc_id == document_id) \
        .delete()
    DB.session.flush()
    DB.session.commit()


def delete_search_history_record_by_search_query(search_query: str):
    """Удаление записи из истории поиска"""
    LOG.debug(f"Enter the delete_search_history_record_by_search_query "
              f"with search_query={search_query}")
    DB.session.query(SearchHistoryRecord) \
        .filter_by(search_query=search_query) \
        .delete()
    DB.session.flush()
    DB.session.commit()


def search_six_documents_from_number(last_doc_number: int) -> list:
    LOG.debug(f"Enter the search_six_documents_from_number with last_doc_number={last_doc_number}")
    six_documents = DB.session.query(DocMetadata) \
        .order_by(DocMetadata.doc_name) \
        .filter(between(DocMetadata.id, last_doc_number, last_doc_number + PROJECT_CONSTANTS.DOCS_COUNT_FOR_UPLOAD - 1)) \
        .all()
    LOG.debug(f"Six documents is {six_documents} start from last_doc_number={last_doc_number}")
    return six_documents


def search_first_four_documents() -> list:
    LOG.debug(f"Enter the search_first_two_documents")
    first_four_documents = DB.session.query(DocMetadata) \
        .order_by(DocMetadata.doc_name) \
        .limit(4) \
        .all()
    LOG.debug(f"First two documents is {first_four_documents}")
    return first_four_documents


def search_document_by_path(path: str) -> DocMetadata:
    """Поиск документов в БД по его полному названию"""
    LOG.debug(f"Enter the search_document_by_path with path={path}")
    document = DB.session.query(DocMetadata) \
        .filter_by(path=path) \
        .first()
    LOG.debug(f"Document with path={path} is {document}")
    return document


def search_first_four_documents_by_partial_name(doc_name: str) -> list:
    """Поиск документов в БД по его частичному названию"""
    LOG.debug(f"Enter the search_first_four_documents_by_partial_name with doc_name={doc_name}")
    documents = DB.session.query(DocMetadata) \
        .filter(DocMetadata.doc_name.contains(doc_name)) \
        .limit(4) \
        .all()
    LOG.debug(f"Documents with doc_name={doc_name} is {documents}")
    return documents


def search_six_documents_by_partial_name_from_number(doc_name: str, last_doc_number: int) -> list:
    """Поиск документов в БД по его частичному названию"""
    LOG.debug(f"Enter the search_first_four_documents_by_partial_name with doc_name={doc_name}")
    documents = DB.session.query(DocMetadata) \
        .filter(and_(DocMetadata.doc_name.contains(doc_name),
                     between(DocMetadata.id, last_doc_number,
                             last_doc_number + PROJECT_CONSTANTS.DOCS_COUNT_FOR_UPLOAD - 1))) \
        .all()
    LOG.debug(f"Documents with doc_name={doc_name} is {documents}")
    return documents


def get_all_search_history_records() -> list:
    """Получение всех записей из истории поиска"""
    LOG.debug(f"Enter the get_all_search_history_records")
    all_search_history_records = DB.session.query(SearchHistoryRecord) \
        .order_by(SearchHistoryRecord.search_time.desc()) \
        .all()
    LOG.debug(f"All founded search_history_records is {all_search_history_records}")
    return all_search_history_records


def get_all_watch_history_records() -> list:
    """Получение всех записей из истории просмотра"""
    LOG.debug(f"Enter the get_all_watch_history_records")
    all_watch_history_records = DB.session.query(WatchHistoryRecord, DocMetadata) \
        .filter(WatchHistoryRecord.doc_id == DocMetadata.id) \
        .order_by(WatchHistoryRecord.watch_time.desc()) \
        .all()
    LOG.debug(f"All founded watch_history_records is {all_watch_history_records}")
    return all_watch_history_records


def get_watch_history_records_by_name(doc_name: str) -> list:
    """Получение записей из истории просмотра по названию документа"""
    LOG.debug(f"Enter the get_watch_history_records_by_name with doc_name={doc_name}")
    watch_history_records = DB.session.query(WatchHistoryRecord, DocMetadata) \
        .filter(and_(WatchHistoryRecord.doc_id == DocMetadata.id, DocMetadata.doc_name.contains(doc_name))) \
        .order_by(WatchHistoryRecord.watch_time.desc()) \
        .all()
    LOG.debug(f"All watch_history_records founded by "
              f"doc_name={doc_name} is {watch_history_records}")
    return watch_history_records


def get_search_history_records_by_name(search_query: str) -> list:
    """Получение записей из истории поиска по названию"""
    LOG.debug(f"Enter the get_all_search_history_records_by_name with search_query={search_query}")
    search_history_records = DB.session.query(SearchHistoryRecord) \
        .filter(SearchHistoryRecord.search_query.contains(search_query)) \
        .order_by(SearchHistoryRecord.search_time.desc()) \
        .all()
    LOG.debug(f"All search_history_records founded by "
              f"search_query={search_query} is {search_history_records}")
    return search_history_records


def add_docmetadata(extension: str, name: str, path: str):
    """Добавление в БД метаданные о документе"""
    LOG.debug(f"Enter the add_docmetadata with extension={extension}, name={name}, path={path}")
    new_doc_metadata = DocMetadata(extension, name, path)
    LOG.debug(f"A new_doc_metadata for adding is {new_doc_metadata}")
    DB.session.add(new_doc_metadata)
    DB.session.commit()
