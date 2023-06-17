from time import sleep

from core.common.bots import BotFather, Watcher
from core.common.enums import State
from core.display.window import WindowHandler

from .children import Mounter


class Gatherer(BotFather):
    def __init__(self):
        self.window = WindowHandler()
        self.mounter = Mounter()
        self.children = [
            self.mounter,
        ]
        self.watcher = Watcher(self.children, "gatherer")

    def start(self):
        self.watcher.start()
        super().start()

    def _start(self):
        while self.running:
            if not self.watcher.running:
                self.stop()

            self.update_search_img()

            if self.state is None:
                self.set_state(State.MOUNTING)
            elif self.state == State.INIT:
                pass
            elif self.state == State.MOUNTING:
                if self.mounter.state == State.DONE:
                    self.set_state(State.SEARCHING)
            elif self.state == State.SEARCHING:
                pass
            elif self.state == State.GATHERING:
                pass
            elif self.state == State.KILLING:
                pass

            sleep(self.MAIN_LOOP_DELAY)
