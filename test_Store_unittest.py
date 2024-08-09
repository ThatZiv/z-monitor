from threading import local
import unittest
from Store import Store
import time
import os


test_db_file = "db-test.db"

class TestStore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = Store(test_db_file)

    @classmethod
    def tearDownClass(cls):
        cls.db.conn.close()
        os.remove(test_db_file)

    def test_today(self):
        # check if today == today
        today = time.localtime().tm_yday
        self.assertEqual(
            time.localtime(self.db.get_today()).tm_yday,
            today)

        # check if [update]  today != today
        day = "2025-01-01 00:00:00"
        today = time.mktime(time.strptime(day, "%Y-%m-%d %H:%M:%S"))
        self.db.update_today(today)
        self.assertNotEqual(
            time.localtime(today).tm_yday,
            time.localtime().tm_yday)

        self.assertEqual(time.localtime(self.db.get_today()).tm_yday,
            time.localtime(today).tm_yday)

    def test_time_used(self):
        self.assertEqual(self.db.get_time_used(), 0)
        self.db.update_time_used(100)
        self.assertEqual(self.db.get_time_used(), 100)

    def test_log(self):
        self.db.log("test")
        self.assertEqual(self.db.get("log", message="test")[0][1], "test")

if __name__ == '__main__':
    unittest.main()
