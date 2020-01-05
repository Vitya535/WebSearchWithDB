"""Файл, в котором реализованы различные сущности БД в виде классов"""

from app import DB
from app import MA
from app.constants import FileExtension


class DocMetadata(DB.Model):
    """Класс, в котором реализованы метаданные для документов"""
    __tablename__ = 'doc_metadata'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    extension = DB.Column(DB.Enum(FileExtension), nullable=False)
    doc_name = DB.Column(DB.String, nullable=False, unique=True)
    path = DB.Column(DB.String, nullable=False, unique=True)
    watch_history_records = DB.relationship("WatchHistoryRecord", backref="doc_metadata", lazy=True)

    def __init__(self, extension, name, path):
        self.extension = extension
        self.doc_name = name
        self.path = path

    def __repr__(self):
        return "DocMetadata(%r, %r, %r, %r)" \
               % (self.id, self.extension, self.doc_name, self.path)


class WatchHistoryRecord(DB.Model):
    """Сущность записи истории просмотра"""
    __tablename__ = 'watch_history_record'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    watch_time = DB.Column(DB.String, nullable=False)
    doc_id = DB.Column(DB.Integer, DB.ForeignKey('doc_metadata.id',
                                                 ondelete="CASCADE",
                                                 onupdate="CASCADE"),
                       nullable=False)

    def __init__(self, search_time, doc_id):
        self.watch_time = search_time
        self.doc_id = doc_id

    def __repr__(self):
        return "WatchHistoryRecord(%r, %r, %r)" % (self.id, self.watch_time, self.doc_id)


class SearchHistoryRecord(DB.Model):
    """Сущность записи истории поиска"""
    __tablename__ = 'search_history_record'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    search_query = DB.Column(DB.String, nullable=False, unique=True)
    search_time = DB.Column(DB.String, nullable=False)

    def __init__(self, search_query, search_time):
        self.search_query = search_query
        self.search_time = search_time

    def __repr__(self):
        return "SearchHistoryRecord(%r, %r, %r)" % (self.id, self.search_query, self.search_time)


class DocMetadataSchema(MA.ModelSchema):
    """Схема для метаданных документов"""

    class Meta:
        """Метаданные для схемы таблицы метаданных документов"""
        model = DocMetadata


class WatchHistoryRecordSchema(MA.ModelSchema):
    """Схема для метаданных истории просмотра"""

    class Meta:
        """Метаданные для схемы таблицы истории просмотра"""
        model = WatchHistoryRecord


class SearchHistoryRecordSchema(MA.ModelSchema):
    """Схема для метаданных истории поиска"""

    class Meta:
        """Метаданные для схемы таблицы истории поиска"""
        model = SearchHistoryRecord


DOC_METADATA_SCHEMA = DocMetadataSchema(many=True)
WATCH_HISTORY_RECORD_SCHEMA = WatchHistoryRecordSchema(many=True)
SEARCH_HISTORY_RECORD_SCHEMA = SearchHistoryRecordSchema(many=True)
