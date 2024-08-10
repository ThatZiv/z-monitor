import psutil

# TODO: do this

class PCInfo:
    def __init__(self):
        self.cpu = psutil.cpu_percent()
        self.memory = psutil.virtual_memory().percent
        self.disk = psutil.disk_usage('/').percent
