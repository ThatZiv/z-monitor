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

    def test_password(self):
        self.assertIsNone(self.db.get_password())

        self.assertRaises(ValueError, self.db.save_password, "passwor")
        self.assertRaises(ValueError, self.db.save_password, "password123")
        self.assertRaises(ValueError, self.db.save_password, "password1234")
        self.assertRaises(ValueError, self.db.save_password, "Password1234")
        self.assertRaises(ValueError, self.db.save_password, "password1234!")
        password = "Password1234!"
        self.db.save_password(password)
        # check if password is saved
        self.assertTrue(self.db.get_password())

        # check if password is correct
        self.assertTrue(self.db.verify_password(password))

    def test_time_limit(self):
        self.assertIsNone(self.db.get_time_limit())
        self.db.set_time_limit(100)
        self.assertEqual(self.db.get_time_limit(), 100)

        self.assertRaises(ValueError, self.db.set_time_limit, 100)
        self.assertRaises(ValueError, self.db.set_time_limit, 24*60*60+1)

        self.assertRaises(ValueError, self.db.set_time_limit, -1)

        self.db.set_time_limit(200)
        self.assertEqual(self.db.get_time_limit(), 200)

if __name__ == '__main__':
    unittest.main()
