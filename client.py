# make sure password prompt is enabled for UAC
# Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorAdmin" -Value 1

import time
import os

import Monitor
import threading
import gui
from Config import config

running = threading.Event()

def track(monitor: Monitor.IoMonitor):
    warnings = config["gui"]["warningTimes"]
    while True:
        try:
            time.sleep(1)
            currentTime = monitor.getTime()
            # 5 minute warning(s)
            print(currentTime)
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
    thread = threading.Thread(target=track, args=(monitor,))
    thread.start()
    monitor.start()


if __name__ == "__main__":
    main()
