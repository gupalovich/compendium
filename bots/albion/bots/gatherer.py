from time import sleep

from core.common.bots import BotFather, Watcher
from core.common.enums import State

from .children import Actionist, Navigator, Visionary


class Gatherer(BotFather):
    def __init__(self):
        self.visionary = Visionary()
        self.actionist = Actionist()
        self.navigator = Navigator()
        self.children = [
            self.visionary,
            # self.actionist,
            # self.navigator,
        ]
        self.watcher = Watcher(self.children, "gatherer")

    def start(self):
        self.watcher.start()
        super().start()

    def prepare_tasks(self):
        pass

    def _start(self):
        """Сделаю пока что проще на if/else создать подходящюю таску"""

        while self.running:
            if not self.watcher.running:
                self.stop()

            if self.state is None:
                self.set_state(State.INIT)
            elif self.state == State.INIT:
                pass
            elif self.state == State.SEARCHING:
                pass
            elif self.state == State.MOVING:
                pass
            elif self.state == State.GATHERING:
                pass
            elif self.state == State.KILLING:
                pass

            sleep(self.MAIN_LOOP_DELAY)
