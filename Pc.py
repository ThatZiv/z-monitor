import psutil
import os
from socket import gethostname

"""
get system information
"""
class Info:
    network_activity = {"sent": 0, "received": 0}
    def get_system_info(self):

        final = {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "network": self.get_net_diff(),
        }
        self.net_sent = psutil.net_io_counters().bytes_sent

        return final

    def get_info(self):
        return {
            "os": os.name,
            "hostname": gethostname(),
        }

    # this will show the network upload/download traffic
    # important: the difference is calculated on-invocation
    #   so first calls will always have a large offset
    def get_net_diff(self):
        bytes_to_mb = lambda b: round(b / 1024 / 1024, 2)
        new_send = psutil.net_io_counters().bytes_sent
        new_recv = psutil.net_io_counters().bytes_recv
        final = {
            "sent": f"{bytes_to_mb(new_send - self.network_activity['sent'])} MB",
            "received": f"{bytes_to_mb(new_recv - self.network_activity['received'])} MB"
        }
        self.network_activity = {"sent": new_send, "received": new_recv}
        return final

    def get_processes(self):
        return [{"name": p.name(), "cpu": p.cpu_percent(), "memory": p.memory_percent()} for p in psutil.process_iter()]

    def get_users(self):
        return [{"name": u.name, "host": u.host} for u in psutil.users()]
