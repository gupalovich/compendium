from time import sleep

from core.common.bots import BotChild
from core.display.vision import Vision
from core.display.window import WindowHandler


class Visionary(BotChild):
    def __init__(self) -> None:
        self.window = WindowHandler()
        self.vision = Vision()
        self.screen = None

    def _start(self):
        while self.running:
            self.screen = self.window.grab()


class Actionist(BotChild):
    def _start(self):
        while self.running:
            sleep(self.MAIN_LOOP_DELAY)


class Navigator(BotChild):
    def _start(self):
        while self.running:
            sleep(self.MAIN_LOOP_DELAY)
