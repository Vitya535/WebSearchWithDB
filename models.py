from sqlalchemy import Column, Enum, String, TIMESTAMP, Integer, ForeignKey
from sqlalchemy.orm import relationship
from utils import FileExtension


class DocMetadata:
    __tablename__ = 'DocMetadata'
    id = Column(Integer, primary_key=True, autoincrement=True)
    extension = Column(Enum(FileExtension), nullable=False)
    name = Column(String, nullable=False, unique=True)
    path = Column(String, nullable=False, unique=True)
    watch_history_records = relationship("WatchHistoryRecord", backref="doc_metadata")
    search_history_records = relationship("SearchHistoryRecord", backref="doc_metadata")

    def __init__(self, extension, name, path):
        self.extension = extension
        self.name = name
        self.path = path

    def __repr__(self):
        return "DocMetadata(%r, %r, %r, %r)" % (self.id, self.extension, self.name, self.path)


class WatchHistoryRecord:
    __tablename__ = 'WatchHistoryRecord'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    img_url = Column(String, nullable=False, unique=True)
    doc_id = Column(Integer, ForeignKey('DocMetadata.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    def __init__(self, name, img_url):
        self.name = name
        self.img_url = img_url

    def __repr__(self):
        return "WatchHistoryRecord(%r, %r, %r)" % (self.id, self.name, self.img_url)


class SearchHistoryRecord:
    __tablename__ = 'SearchHistoryRecord'
    id = Column(Integer, primary_key=True, autoincrement=True)
    search_query = Column(String, nullable=False, unique=True)
    search_time = Column(TIMESTAMP, nullable=False)
    doc_id = Column(Integer, ForeignKey('DocMetadata.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    def __init__(self, search_query, search_time):
        self.search_query = search_query
        self.search_time = search_time

    def __repr__(self):
        return "SearchHistoryRecord(%r, %r, %r)" % (self.id, self.search_query, self.search_time)
