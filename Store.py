import time
from Database import Database
from Config import config
from getpass import getpass
import bcrypt

class Store(Database):
    def __init__(self, db_file=config['db']):
        super().__init__(db_file)

        self.insert("log", message="program startup", _timestamp=str(time.time()))

        # check if config.today exists
        today_resp = self.get_today()
        today = str(time.time())
        if not today_resp:
            self.insert("store", name="today", value=today)
        else:
            # reset time_used if new day
            lct = lambda x: time.localtime(float(x))
            if lct(today_resp).tm_yday != lct(today).tm_yday:
                self.update_today(today)
                self.update_time_used(0)

        # checks if time_used exists
        time_limit = self.get("store", name="time_used")
        if not time_limit:
            self.insert("store", name="time_used", value="0")
            time_limit = "0"
        else:
            time_limit = time_limit[0][1]

    """
    Saves the master password to the database
    """
    def get_today(self):
        today = self.get("store", name="today")
        if not today:
            return None
        return float(today[0][1])

    """
    Returns the time limit for the user (in seconds)
    """
    def get_time_limit(self):
        limit = self.get("store", name="time_limit")
        if limit:
            return int(limit[0][1])
        else:
            return None

    """
    Sets the time limit for the user (in seconds)
    """
    def set_time_limit(self, time_limit=config["timeLimit"]):
        current_limit = self.get_time_limit()
        if time_limit == current_limit:
            raise ValueError("Time limit is already set to this value")
        elif time_limit < 0:
            raise ValueError("Time limit must be greater than 0")
        elif time_limit >= 60*60*24:
            raise ValueError("Time limit must be less than 24 hours")

        if not current_limit:
            self.insert("store", name="time_limit", value=str(time_limit))
        else:
            self.update("store", where_key="name", where_value="time_limit", value=str(time_limit))

    def update_time_used(self, time_used):
        self.update("store", where_key="name", where_value="time_used", value=str(time_used))

    def update_today(self, today) -> None:
        self.update("store", where_key="name", where_value="today", value=str(today))

    def get_time_used(self):
        time_used = self.get("store", name="time_used")
        if time_used:
            return int(time_used[0][1])
        else:
            self.update_time_used(0)
            return 0

    def log(self, message: str, type: str = "info"):
        self.insert("log", message=message, _timestamp=str(time.time()), type=type)

    def get_logs(self, page: int = 0, limit: int = 50):
        self.cur.execute(f"SELECT COUNT(*) FROM log")
        count = self.cur.fetchone()[0]
        self.cur.execute(f"SELECT * FROM log ORDER BY '_timestamp' DESC LIMIT {limit} OFFSET {page*limit}")

        return {
            'count': count,
            'page': page,
            'limit': limit,
            'last': page*limit >= count,
            'content': self.cur.fetchall()
        }

    """
    Returns the master password if it exists, otherwise None.
    """
    def get_password(self):
        password = self.get("store", name="master_password")
        if password:
            return password[0][1]
        return None

    """
    Prompts the user to set/update a master password.
    """
    def save_password(self, password):
        symbols = "!@#$%^&*()_+"
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        elif not any([char in symbols for char in password]):
            raise ValueError(f"Password must contain at least one special character ({symbols})")
        elif not any([char.isupper() for char in password]):
            raise ValueError("Password must contain at least one uppercase letter")
        elif not any([char.isdigit() for char in password]):
            raise ValueError("Password must contain at least one number")

        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(password.encode(), salt)
        if not self.get_password():
            self.insert("store", name="master_password", value=password.decode())
        else:
            self.update("store", where_key="name", where_value="master_password", value=password.decode())

    def verify_password(self, password):
        current_password = self.get_password()
        if current_password:
            return bcrypt.checkpw(password.encode(), current_password.encode())
        else:
            return False
