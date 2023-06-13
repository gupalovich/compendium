from time import sleep
from typing import Callable

from pynput import keyboard

from .abc import BotFather, BotMother
from .children import Actionist, Visionary

# from core.common.enums import State


class Watcher(BotMother):
    def __init__(self, on_release_type: str = None):
        self._set_on_release(on_release_type)

    def _set_on_release(self, on_release_type: str):
        match on_release_type:
            case "gatherer":
                self.on_release = self.gatherer_on_release
            case _:
                self.on_release = self._on_release

    def gatherer_on_release(self, key: keyboard.Key):
        if key == keyboard.Key.esc:
            self.stop()
            return False
        return True

    def _on_release(self, key: keyboard.Key):
        if key == keyboard.Key.end:
            self.stop()
            return False
        return True

    def start(self):
        super().start()
        self._start()

    def _start(self):
        listener = keyboard.Listener(on_release=self.on_release)
        listener.start()


class Gatherer(BotFather):
    def __init__(self):
        self.key_binds = {
            "exit": keyboard.Key.esc,
        }
        self.children = [Visionary(), Actionist()]
        self.watcher = Watcher("gatherer")

    def start(self):
        super().start()
        self.watcher.start()
        self.start_children()
        self._start()

    def stop(self):
        super().stop()
        self.stop_children()

    def _start(self):
        while self.running:
            sleep(self.MAIN_LOOP_DELAY)

            if not self.watcher.running:
                self.stop()
