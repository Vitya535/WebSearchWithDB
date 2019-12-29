"""Файл для создания БД в SQLite"""
from sqlite3 import connect

CONN = connect('documents.db')

CURSOR = CONN.cursor()

CURSOR.execute("""PRAGMA foreign_keys = ON""")

CURSOR.execute("""CREATE TABLE if not exists doc_metadata
                (id integer PRIMARY KEY AUTOINCREMENT,
                 extension text CHECK (extension in ('doc', 'pdf', 'docx', 'txt') NOT NULL),
                 doc_name text NOT NULL,
                 path text NOT NULL,
                 img_url text NOT NULL
                 CONSTRAINT unique_doc_metadata UNIQUE (name, path))
               """)

CURSOR.execute("""CREATE TABLE if not exists watch_history_record
                (id integer PRIMARY KEY AUTOINCREMENT,
                search_time text NOT NULL,
                doc_id integer,
                FOREIGN KEY (doc_id) REFERENCES doc_metadata(id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT unique_watch_history_record UNIQUE (name, img_url))
               """)

CURSOR.execute("""CREATE TABLE if not exists search_history_record
                (id integer PRIMARY KEY AUTOINCREMENT,
                search_query text NOT NULL,
                search_time text NOT NULL,
                CONSTRAINT unique_search_history_record UNIQUE (search_query))
               """)

CONN.commit()
CONN.close()
