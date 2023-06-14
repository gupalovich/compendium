from time import sleep

from core.common.bots import BotFather, Watcher
from core.common.entities import Action, Search, Task
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

        self.tasks = [
            Task(
                "Find main character",
                nodes=[
                    Search(self.prepare_tasks, args=(self.visionary.screen)),
                    Action(self.prepare_tasks),
                ],
                one_off=False,
                use_state=None,
            ),
            Task(
                "To mount",
                nodes=[],
                one_off=False,
                use_state=State.INIT,
            ),
        ]
        self.active_tasks = []

    def start(self):
        self.watcher.start()
        super().start()

    def prepare_tasks(self):
        pass

    def _start(self):
        while self.running:
            if not self.watcher.running:
                self.stop()

            if self.state is None:
                if not self.tasks:
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
