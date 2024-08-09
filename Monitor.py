from pynput import mouse, keyboard
import threading
import time
from Logger import Logger
from Config import config
from Store import Store

class Monitor:

    def __init__(self):
        self.config = config
        self.bufferSec = self.config["bufferSec"]
        self.timeLimit = self.config["timeLimit"]
        self.store = Store()
        self.logger = Logger(self.store)

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
            self.logger.log(self.keystrokeBuffer)
            self.keystrokeBuffer = ""
        self.lastTyped = time.time()


    def start(self):
        threading.Thread(target=self.mouseListener.join).start()
        threading.Thread(target=self.keyboardListener.join).start()




# class KeyboardMonitor(Monitor):
#     def __init__(self, bufferSec = 5):
#         super().__init__(bufferSec)
#         self.mouseListener = keyboard.Listener(on_press=self.on_press)
#         self.mouseListener.start()

#     def on_press(self, key):
#         self.addTime(self.bufferSec)

#     def start(self):
#         self.mouseListener.join()
