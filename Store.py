import time
from Database import Database
from Config import config

class Store(Database):
    def __init__(self):
        super().__init__(config['db'])

        self.insert("log", message="program startup", _timestamp=str(time.time()))

        # check if config.today exists
        today_resp = self.get_today()
        today = str(time.time())
        if not today_resp:
            self.insert("store", name="today", value=today)
        else:
            lct = lambda x: time.localtime(float(x))
            if lct(today_resp[0][1]).tm_yday != lct(today).tm_yday:
                self.update_today(today)
                self.update_time_used(0)

        # checks if time_used exists
        time_limit = self.get("store", name="time_used")
        if not time_limit:
            self.insert("store", name="time_used", value="0")
            time_limit = "0"
        else:
            time_limit = time_limit[0][1]

    def get_today(self):
        today = self.get("store", name="today")

    def update_time_used(self, time_used):
        self.update("store", where_key="name", where_value="time_used", value=str(time_used))

    def update_today(self, today):
        self.update("store", where_key="name", where_value="today", value=today)

    def get_time_used(self):
        time_used = self.get("store", name="time_used")
        if time_used:
            return int(time_used[0][1])
        else:
            self.update_time_used(0)
            return 0
