from sqlite3 import connect

conn = connect('documents.db')

cursor = conn.cursor()

cursor.execute("""PRAGMA foreign_keys = ON""")

cursor.execute("""CREATE TABLE if not exists doc_metadata
                (id integer PRIMARY KEY AUTOINCREMENT,
                 extension text CHECK (extension in ('doc', 'pdf', 'docx', 'txt') NOT NULL)
                 name text NOT NULL,
                 path text NOT NULL,
                 CONSTRAINT unique_doc_metadata UNIQUE (name, path))
               """)

cursor.execute("""CREATE TABLE if not exists watch_history_record
                id integer PRIMARY KEY AUTOINCREMENT,
                name text NOT NULL,
                img_url text NOT NULL,
                FOREIGN KEY (doc_id) REFERENCES doc_metadata(id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT unique_watch_history_record UNIQUE (name, img_url)
               """)

cursor.execute("""CREATE TABLE if not exists search_history_record
                id integer PRIMARY KEY AUTOINCREMENT,
                search_query text NOT NULL,
                search_time text NOT NULL,
                FOREIGN KEY (doc_id) REFERENCES doc_metadata(id) ON DELETE CASCADE ON UPDATE CASCADE,
                CONSTRAINT unique_search_history_record UNIQUE (search_query)
               """)

conn.commit()
conn.close()
