"""
This should be run on startup. Take a look @
https://stackoverflow.com/questions/32404/how-do-you-run-a-python-script-as-a-service-in-windows
"""

__author__ = "Lukas Mahler"
__version__ = "0.0.1"
__date__ = "02.09.2021"
__email__ = "m@hler.eu"
__status__ = "Development"


import os
import ctypes
from pystray import Icon, Menu as Menu, MenuItem as Item
from PIL import Image
import threading


class MyTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class MyTray:

    def __init__(self):

        self.cooldown = 5 # 3600

        self.state = False
        self.logo = Image.open(r"img\pillow.png")
        self.mymenu = Menu(
            Item('Pause', lambda: self.pause(), default=True),
            Item('Resume', lambda: self.resume()),
            Item('Settings', lambda: self.settings(), checked=lambda item: self.state),
            Menu.SEPARATOR,
            Item('Quit', lambda: self.quit())
        )
        self.icon = Icon("PauseChampy", self.logo, "PauseChampy", self.mymenu)
        self.timer = self.maketimer()
        self.timer.start()

    def maketimer(self):
        timer = MyTimer(self.cooldown, self.alert)
        timer.daemon = True
        return timer

    def start(self):
        self.icon.icon = Image.open(r"img\pillow_on.png")
        self.icon.run()

    def pause(self):
        print(self.icon.HAS_NOTIFICATION)
        self.icon.notify("test")
        self.icon.icon = Image.open(r"img\pillow_pause.png")
        self.timer.cancel()

    def resume(self):
        self.icon.icon = Image.open(r"img\pillow_on.png")
        self.timer = self.maketimer()
        self.timer.start()

    def stop(self):
        self.icon.icon = Image.open(r"img\pillow_off.png")

    def settings(self):
        pass

    def quit(self):
        self.timer.cancel()
        self.icon.stop()

    @staticmethod
    def alert():
        mbox("Take a break please")


def mbox(tx):
    """
    Non blocking version using an extra thread
    Using daemon=True kills the thread when the main program dies
    """
    popup = ctypes.windll.user32.MessageBoxW
    threading.Thread(daemon=True, target=lambda: popup(0, tx, "PauseChampy", 64)).start()


def main():
    # Only supporting windows
    if os.name != "nt":
        exit()
    tray = MyTray()
    tray.start()


if __name__ == '__main__':
    main()
