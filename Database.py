import sqlite3
import time
from threading import Lock

queries = {
    "init": f"""
CREATE TABLE IF NOT EXISTS store (
    name TEXT PRIMARY KEY,
    value TEXT
)

CREATE TABLE IF NOT EXISTS log (
    id INTEGER PRIMARY KEY,
    message TEXT,
    _timestamp REAL,
    type TEXT DEFAULT "info"
)
"""
}


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db, check_same_thread=False)
        self.lock = Lock()
        self.cur = self.conn.cursor()
        self._init_database()

    def _init_database(self):
        try:
            self.lock.acquire(True)
            for table_query in queries["init"].split("\n\n"):
                self.cur.execute(table_query)
            self.conn.commit()
        finally:
            self.lock.release()

    def __del__(self):
        self.conn.close()

    def insert(self, table, **kwargs):
        try:
            self.lock.acquire(True)
            columns = kwargs.keys()
            values = kwargs.values()
            if len(columns) != len(values):
                raise ValueError("columns and values must be of equal length")
            prefills = ("?,"*len(columns))[:-1]
            self.cur.execute(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({prefills})", list(values))
            self.conn.commit()
        finally:
            self.lock.release()

    def update(self, table, where_key, where_value, **kwargs):
        try:
            self.lock.acquire(True)
            columns = kwargs.keys()
            values = kwargs.values()
            prefills = ", ".join([f"{column} = ?" for column in columns])
            self.cur.execute(f"UPDATE {table} SET {prefills} WHERE {where_key} = ?", [*values, where_value])
            self.conn.commit()
        finally:
            self.lock.release()

    def get(self, table, **kwargs):
        try:
            self.lock.acquire(True)
            columns = kwargs.keys()
            values = kwargs.values()
            if not columns:
                self.cur.execute(f"SELECT * FROM {table}")
                return self.cur.fetchall()
            prefills = " AND ".join([f"{column} = ?" for column in columns])
            self.cur.execute(f"SELECT * FROM {table} WHERE {prefills}", list(values))
            return self.cur.fetchall()
        finally:
            self.lock.release()
