# make sure password prompt is enabled for UAC
# Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" -Name "ConsentPromptBehaviorAdmin" -Value 1

import time
import os

import Monitor
import threading
import gui

appName = "z"
def checkTime(monitor: Monitor.IoMonitor):
    warningTimes = [60*5, 60*2, 60*1]
    while True:
        time.sleep(1)
        currentTime = monitor.getTime()
        # 5 minute warning
        # for warning in warningTimes:
        #     if currentTime >= monitor.timeLimit - warning:
        #         gui.alert(f"{warning//60} minutes remaining")
        #         warningTimes.remove(warning)
        if currentTime >= monitor.timeLimit:
            gui.alert("Time limit exceeded. Shutting down...")

            monitor.resetTime()

            # if os.name == "nt":
            #     os.system("shutdown /s /t 1")
            # elif os.name == "posix":
            #     os.system("shutdown -h now")

        print(monitor.getTime(), monitor.keystrokeBuffer)

def main():
    monitor = Monitor.IoMonitor()
    thread = threading.Thread(target=checkTime, args=(monitor,))
    thread.start()
    monitor.start()



if __name__ == "__main__":
    main()
