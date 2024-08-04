from os import path
import logging

class Logger:
    def __init__(self):
        logging.basicConfig(filename=path.join(path.dirname(__file__),
            "log.txt"),
            level=logging.INFO,
            format=f"[%(asctime)s]: %(name)s - %(levelname)s \n%(message)s"
        )
        self.logger = logging.getLogger("Monitor")

    def log(self, message: str):
        print(message)
        self.logger.info(msg=message)
