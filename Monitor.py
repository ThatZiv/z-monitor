from pynput import mouse, keyboard
import threading
import time
from getpass import getpass
from Logger import Logger
from Config import config
from Store import Store
import sys

class Monitor:

    def __init__(self):
        self.config = config
        self.bufferSec = self.config["bufferSec"]
        self.store = Store()
        self.logger = Logger(self.store)

        if not self.store.get_password():
            self.store.save_password(config['defaultPassword'])
        if not self.store.get_time_used():
            self.store.update_time_used(0)
        if not self.store.get_time_limit():
            self.store.set_time_limit(config["timeLimit"])


    def start(self):
        pass

    def addTime(self, time: int):
        if not time:
            time = self.bufferSec
        self.store.update_time_used(self.getTime() + time)

    def resetTime(self):
        self.store.update_time_used(0)

    def getTime(self):
        return self.store.get_time_used()


class IoMonitor(Monitor):
    def __init__(self):
        super().__init__()
        self.lastMoved = time.time()
        self.lastTyped = time.time()
        self.keystrokeBuffer = ""
        self.keystrokeBufferSec = self.config["keystrokeBufferSec"]
        self.mouseListener = mouse.Listener(on_move=self.on_interact)
        self.keyboardListener = keyboard.Listener(on_press=self.on_keypress)
        # self.mouseListener.start()
        # self.keyboardListener.start()
        # start both listeners in seperate threads

        self.mouseListener.start()
        self.keyboardListener.start()

    # keep track of time usage
    def on_interact(self, *args):
        if time.time() - self.lastMoved > self.bufferSec:
            self.lastMoved = time.time()
            # crappy way to keep track of time usage
            self.addTime(self.bufferSec)

    def on_keypress(self, key):
        self.on_interact()
        try:
            self.keystrokeBuffer += key.char
        except AttributeError:
            if key == keyboard.Key.space:
                self.keystrokeBuffer += " "
            elif key == keyboard.Key.enter:
                self.keystrokeBuffer += "\n"
            # elif key == keyboard.Key.backspace:
            #     self.keystrokeBuffer = self.keystrokeBuffer[:-1]
            elif key == keyboard.Key.esc:
                self.keystrokeBuffer = ""
            else:
                self.keystrokeBuffer += f"<{key}>"

        if time.time() - self.lastTyped > self.keystrokeBufferSec:
            self.logger.log(self.keystrokeBuffer, type="keystroke")
            self.keystrokeBuffer = ""
        self.lastTyped = time.time()


    def start(self):
        threading.Thread(target=self.mouseListener.join).start()
        threading.Thread(target=self.keyboardListener.join).start()
