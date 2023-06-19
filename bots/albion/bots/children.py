from time import sleep

from core.common.bots import BotChild
from core.common.enums import State

from ..actions.mount import MountActions, MountVision


class Mounter(BotChild):
    def __init__(self) -> None:
        super().__init__(MountVision)
        self.actions = MountActions()

    def manage_state(self):
        match (self.state):
            case State.IDLE:
                pass
            case State.START:
                if self.vision.is_mounting(self.search_img):
                    print("Mounting")
                elif self.vision.is_mounted(self.search_img):
                    print("On mount")  # release control
                else:
                    print("Gonna mount")
                self.set_state(State.DONE)
            case State.DONE:
                pass


class Navigator(BotChild):
    def __init__(self) -> None:
        super().__init__(MountVision)


class Gatherer(BotChild):
    def __init__(self) -> None:
        super().__init__(MountVision)

    def manage_state(self):
        match (self.state):
            case State.IDLE:
                pass
            case State.START:
                if not self.targets:
                    self.set_state(State.DONE)
            case State.DONE:
                pass
