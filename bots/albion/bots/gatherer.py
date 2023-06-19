from time import sleep

from core.common.bots import BotFather, Watcher
from core.common.enums import State
from core.display.window import WindowHandler

from .children import BotChild, Gatherer, Mounter, Navigator


class GathererFather(BotFather):
    def __init__(self):
        self.window = WindowHandler()
        self.mounter = Mounter()
        self.navigator = Navigator()
        self.gatherer = Gatherer()
        self.children += [self.mounter, self.navigator, self.gatherer]
        self.watcher = Watcher(self.children, on_release_type="gatherer")

    def manage_active_child(self, child: BotChild, next_state: State):
        if child.state == State.IDLE:
            self.active_child = child
            self.active_child.set_state(State.START)
        if child.state == State.DONE:
            self.active_child.set_state(State.IDLE)
            self.active_child = None
            self.set_state(next_state)

    def manage_state(self):
        match (self.state):
            case None:
                self.set_state(State.INIT)
                self.set_children_state(State.IDLE)
            case State.INIT:
                # Check game client, weight, location, etc...
                self.set_state(State.MOUNTING)
            case State.MOUNTING:
                self.manage_active_child(
                    self.mounter,
                    next_state=State.NAVIGATING,
                )
            case State.NAVIGATING:
                self.manage_active_child(
                    self.navigator,
                    next_state=State.NAVIGATING,
                )
            case State.GATHERING:
                pass
            case _:
                self.set_state(None)

    def start(self):
        self.watcher.start()
        super().start()

    def _start(self):
        while self.running:
            if not self.watcher.running:
                self.stop()

            self.update_search_img()
            self.update_children_search_img()
            self.manage_state()

            sleep(self.MAIN_LOOP_DELAY)
