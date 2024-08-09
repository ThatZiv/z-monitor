from os import path
import logging
from Store import Store

class Logger:
    def __init__(self, store: Store):
        logging.basicConfig(filename=path.join(path.dirname(__file__),
            "log.txt"),
            level=logging.INFO,
            format=f"[%(asctime)s]: %(name)s - %(levelname)s \n%(message)s",
        )
        self.logger = logging.getLogger("Monitor")
        self.store = store

    def log(self, message: str):
        print(message)
        self.store.log(message)
        self.logger.info(msg=message)
