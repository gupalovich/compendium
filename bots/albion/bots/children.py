from time import sleep

from core.display.vision import VisionBase
from core.display.window import WindowHandler

from .abc import BotChild


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


class Navigator(BotChild):
    pass
