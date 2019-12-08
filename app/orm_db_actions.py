"""Файл с запросами к БД"""

from app import DB
from app.models import DocMetadata
from app.models import SearchHistoryRecord
from app.models import WatchHistoryRecord


def delete_watch_history_record_by_name(record_name):
    """Удаление записи из истории просмотра"""
    DB.session.query(WatchHistoryRecord)\
        .filter_by(name=record_name).delete()
    DB.session.flush()
    DB.session.commit()


def delete_search_history_record_by_name(search_query):
    """Удаление записи из истории поиска"""
    DB.session.query(SearchHistoryRecord)\
        .filter_by(search_query=search_query).delete()
    DB.session.flush()
    DB.session.commit()


def search_all_documents():
    """Поиск всех документов в БД"""
    all_documents = DB.session.query(DocMetadata).all()
    return all_documents


def search_documents_by_name(doc_name):
    """Поиск документов в БД по названию"""
    documents = DB.session.query(DocMetadata)\
        .filter_by(doc_name=doc_name).all()
    return documents


def get_all_search_history_records():
    """Получение всех записей из истории поиска"""
    all_search_history_records = DB.session.query(SearchHistoryRecord).all()
    return all_search_history_records


def get_all_watch_history_records():
    """Получение всех записей из истории просмотра"""
    all_watch_history_records = DB.session.query(WatchHistoryRecord).all()
    return all_watch_history_records


def get_watch_history_records_by_name(record_name):
    """Получение записей из истории просмотра по названию"""
    watch_history_records = DB.session.query(WatchHistoryRecord)\
        .filter_by(name=record_name).all()
    return watch_history_records


def get_search_history_records_by_name(search_query):
    """Получение записей из истории поиска по названию"""
    search_history_records = DB.session.query(SearchHistoryRecord)\
        .filter_by(search_query=search_query).all()
    return search_history_records
