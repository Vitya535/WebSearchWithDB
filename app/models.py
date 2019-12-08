"""Файл, в котором реализованы различные сущности БД в виде классов"""

from app import DB
from app.utils import FileExtension


class DocMetadata(DB.Model):
    """Класс, в котором реализованы метаданные для документов"""
    __tablename__ = 'doc_metadata'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    extension = DB.Column(DB.Enum(FileExtension), nullable=False)
    doc_name = DB.Column(DB.String, nullable=False, unique=True)
    path = DB.Column(DB.String, nullable=False, unique=True)
    watch_history_records = DB.relationship("WatchHistoryRecord", backref="doc_metadata")
    search_history_records = DB.relationship("SearchHistoryRecord", backref="doc_metadata")

    def __init__(self, extension, name, path):
        self.extension = extension
        self.doc_name = name
        self.path = path

    def __repr__(self):
        return "DocMetadata(%r, %r, %r, %r)" % (self.id, self.extension, self.doc_name, self.path)


class WatchHistoryRecord(DB.Model):
    """Сущность записи истории просмотра"""
    __tablename__ = 'watch_history_record'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String, nullable=False, unique=True)
    img_url = DB.Column(DB.String, nullable=False, unique=True)
    doc_id = DB.Column(DB.Integer, DB.ForeignKey('doc_metadata.id',
                                                 ondelete="CASCADE",
                                                 onupdate="CASCADE"),
                       nullable=False)

    def __init__(self, name, img_url):
        self.name = name
        self.img_url = img_url

    def __repr__(self):
        return "WatchHistoryRecord(%r, %r, %r)" % (self.id, self.name, self.img_url)


class SearchHistoryRecord(DB.Model):
    """Сущность записи истории поиска"""
    __tablename__ = 'search_history_record'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    search_query = DB.Column(DB.String, nullable=False, unique=True)
    search_time = DB.Column(DB.TIMESTAMP, nullable=False)
    doc_id = DB.Column(DB.Integer, DB.ForeignKey('doc_metadata.id',
                                                 ondelete="CASCADE",
                                                 onupdate="CASCADE"),
                       nullable=False, default=None)

    def __init__(self, search_query, search_time):
        self.search_query = search_query
        self.search_time = search_time

    def __repr__(self):
        return "SearchHistoryRecord(%r, %r, %r)" % (self.id, self.search_query, self.search_time)
