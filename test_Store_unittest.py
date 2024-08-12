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
        self.db.log("test1")
        self.assertEqual(self.db.get("log", message="test1")[0][1], "test1")

        self.db.log("test2", "ui")
        self.db.log("test3", "keystroke")
        self.db.log("test4", "ui")
        self.db.log("test5", "info")
        self.db.log("test6", "info")
        self.db.log("test7", "info")
        self.db.log("test8", "info")
        self.db.log("test9", "info")
        self.db.log("test10", "info")

        # test pagination
        page = 0
        while page < 5:
            logs_resp = self.db.get_logs(page=page, limit=2)
            self.assertEqual(len(logs_resp['content']), 2)
            self.assertEqual(logs_resp['count'], 10)
            self.assertEqual(logs_resp['page'], page)
            self.assertEqual(logs_resp['limit'], 2)
            self.assertEqual(logs_resp['content'][0][1], f"test{10 - page * 2}")
            if page == 5:
                self.assertTrue(logs_resp['last'])
            page += 1

        logs = self.db.get_logs(type=['info'])
        self.assertEqual(logs['count'], 7)
        logs = self.db.get_logs(type=['ui'])
        self.assertEqual(logs['count'], 2)
        logs = self.db.get_logs(type=['keystroke', 'ui'])
        self.assertEqual(logs['count'], 3)




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
