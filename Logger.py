from os import path
import logging
from Store import Store
from Config import config

class Logger:
    def __init__(self, store: Store):
        logging.basicConfig(
            filename="log.txt",
            level=logging.INFO,
            format=f"[%(asctime)s]: %(name)s - %(levelname)s \n%(message)s",
        )
        self.logger = logging.getLogger("Monitor")
        self.store = store

    def log(self, message: str):
        if config["env"] == "dev":
            print(message)
        self.store.log(message)
        self.logger.info(msg=message)
