from time import sleep

from pynput import keyboard

# from core.common.enums import State
from core.display.vision import VisionBase
from core.display.window import WindowHandler

from .abc import BotChild, BotFather, BotMother


class Watcher(BotMother):
    def __init__(self, keys: dict = None):
        self.key_binds = keys or {
            "exit": keyboard.Key.esc,
        }

    def on_release(self, key):
        if key == self.key_binds["exit"]:
            self.stop()
            return False

    def start(self):
        super().start()
        self._start()

    def _start(self):
        listener = keyboard.Listener(on_release=self.on_release)
        listener.start()


class Visionary(BotChild):
    def __init__(self) -> None:
        self.window = WindowHandler()
        self.vision = VisionBase()

    def _start(self):
        while self.running:
            sleep(self.MAIN_LOOP_DELAY)


class Actionist(BotChild):
    def _start(self):
        while self.running:
            sleep(self.MAIN_LOOP_DELAY)


class Gatherer(BotFather):
    def __init__(self):
        self.key_binds = {
            "exit": keyboard.Key.esc,
        }
        self.children = [Visionary(), Actionist()]
        self.watcher = Watcher(self.key_binds)

    def start(self):
        super().start()
        self.watcher.start()
        self._start()
        self.start_children()

    def stop(self):
        super().stop()
        self.stop_children()

    def _start(self):
        while self.running:
            sleep(self.MAIN_LOOP_DELAY)

            if not self.watcher.running:
                self.stop()
