# make sure password prompt is enabled for UAC
# Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorAdmin" -Value 1

import time
import os

import Monitor
import threading
import gui
from Config import config
from Webserver import Webserver

def run_webserver(webserver: Webserver):
    webserver.run()

def track(monitor: Monitor.IoMonitor):
    warnings = config["gui"]["warningTimes"]
    while True:
        try:
            time.sleep(1)
            currentTime = monitor.getTime()
            if config["env"] == "dev": print(currentTime)
            # warning notifications
            if len(warnings) > 0:
                warning = warnings[-1]
                if currentTime >= monitor.timeLimit - warning:
                    warningStr = f"{warning//60} minutes remaining"
                    gui.alert(warningStr)
                    monitor.logger.log(warningStr)
                    warnings.pop()
            if currentTime >= monitor.timeLimit:
                gui.alert("Time limit exceeded. Shutting down...")
                monitor.logger.log("Time limit exceeded. Shutting down...")

                if config['env'] == "prod":
                    if os.name == "nt":
                        os.system("shutdown /s /t 1")
                    elif os.name == "posix":
                        os.system("shutdown -h now")
        except Exception as e:
            monitor.logger.log(f"Error: {e}")
            continue

    monitor.store.conn.close()



def main():
    monitor = Monitor.IoMonitor()
    webserver = Webserver(monitor.store)
    thread = threading.Thread(target=track, args=(monitor,))
    webserver_thread = threading.Thread(target=run_webserver, args=(webserver,))
    webserver_thread.start()
    thread.start()
    monitor.start()


if __name__ == "__main__":
    main()
