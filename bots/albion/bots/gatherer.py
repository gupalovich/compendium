from time import sleep

from core.common.bots import BotFather, Watcher
from core.common.enums import State

from .children import Actionist, Navigator, Visionary


class Gatherer(BotFather):
    def __init__(self):
        self.visionary = Visionary()
        self.actionist = Actionist()
        self.navigator = Navigator()
        self.children = [self.visionary, self.actionist, self.navigator]
        self.watcher = Watcher(self.children, "gatherer")

    def start(self):
        self.watcher.start()
        super().start()

    def _start(self):
        while self.running:
            if not self.watcher.running:
                self.stop()
            # self.update_children_state()
            sleep(self.MAIN_LOOP_DELAY)
