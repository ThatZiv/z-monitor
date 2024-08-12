import unittest
from Database import Database
import time
import os

test_db_file = "db-test.db"

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Database(test_db_file)

    def test_insert(self):
        self.db.insert("store", name="test", value="test")
        self.assertEqual(self.db.get("store", name="test"), [("test", "test")])
        self.db.insert("log", message="test", _timestamp="test")
        self.assertEqual(self.db.get("log", message="test"), [(1, "test", "test", 'info')])
        self.db.insert("log", message="test2", _timestamp="test2", type="ui")
        self.assertEqual(self.db.get("log"), [(1, "test", "test", 'info'), (2, "test2", "test2", "ui")])

    def test_update(self):
        name = "key"
        value = "123"
        updated_value = "124"
        self.db.insert("store", name=name, value=value)
        self.db.update("store", where_key="name", where_value=name, value=updated_value)
        self.assertEqual(self.db.get("store", name=name), [(name, updated_value)])

    @classmethod
    def tearDownClass(cls):
        cls.db.conn.close()
        os.remove(test_db_file)

if __name__ == '__main__':
    unittest.main()
