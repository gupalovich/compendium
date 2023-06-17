from time import sleep

from core.common.bots import BotChild
from core.common.enums import State

from ..actions.mount import MountActions, MountVision


class Mounter(BotChild):
    def __init__(self) -> None:
        super().__init__(MountVision)
        self.actions = MountActions()

    def _start(self):
        while self.running:
            if self.state != State.MOUNTING:
                sleep(self.PAUSE_DELAY)
                continue

            if self.vision.is_mounting(self.search_img):
                print("Mounting")
            elif self.vision.is_mounted(self.search_img):
                print("On mount")  # release control
            else:
                print("Gonna mount")
                sleep(1)
                self.set_state(State.DONE)


class Navigator(BotChild):
    def _start(self):
        while self.running:
            sleep(self.MAIN_LOOP_DELAY)


class Killer(BotChild):
    """
    passive/aggressive mode
    if not in_control - deeper sleep
    """

    def _start(self):
        while self.running:
            sleep(self.MAIN_LOOP_DELAY)
