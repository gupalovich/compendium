from time import sleep

from pynput import keyboard

from core.common.enums import State

from .abc import BotFather, BotMother
from .children import Actionist, Navigator, Visionary


class Watcher(BotMother):
    def __init__(self, on_release_type: str = ""):
        self._set_on_release(on_release_type)

    def _set_on_release(self, on_release_type: str):
        if not isinstance(on_release_type, str):
            raise ValueError("Incorrect on_release_type: ", on_release_type)

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
        self.watcher = Watcher("gatherer")
        self.visionary = Visionary()
        self.actionist = Actionist()
        self.navigator = Navigator()
        self.children = [self.visionary, self.actionist, self.navigator]

    def start(self):
        super().start()
        self.watcher.start()
        self._start()

    def _start(self):
        while self.running:
            if not self.watcher.running:
                self.stop()
            print(self.visionary.screen)
            # self.update_children_state()
            sleep(self.MAIN_LOOP_DELAY)
