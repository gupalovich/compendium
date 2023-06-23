from time import sleep

from core.common.bots import BotChild
from core.common.enums import State

from ..actions.input import AlbionActions, log
from ..actions.vision import GathererVision, MounterVision, NavigatorVision


class Mounter(BotChild):
    def __init__(self) -> None:
        super().__init__(AlbionActions, MounterVision)

    def manage_state(self):
        if self.state == State.START:
            is_mounting = self.vision.is_mounting(self.search_img)
            is_mounted = self.vision.is_mounted(self.search_img)

            if is_mounting:
                log("Mounting", delay=0.3)
            elif is_mounted:
                log("Mounted")
                self.set_state(State.DONE)
            else:
                self.actions.mount()
                log("Trying to mount")
        else:
            sleep(0.2)


class Gatherer(BotChild):
    def __init__(self) -> None:
        super().__init__(AlbionActions, GathererVision)

    def update_target(self):
        self.targets = []

    def manage_state(self):
        if not self.state:
            return

        self.targets = self.vision.yolo.find(self.search_img, confidence=0.7)

        if self.state == State.START:
            is_gathering = self.vision.is_gathering(self.search_img)
            if self.targets:
                target = self.vision.find_closest(self.targets)
                self.actions.gather(target.center)
                log(f"Trying to gather [{target.label}]")
            if is_gathering:
                log("Gathering", delay=0.3)
            if not is_gathering and not self.targets:
                log("Done gathering")
                self.set_state(State.DONE)
        else:
            sleep(0.2)


class Navigator(BotChild):
    def __init__(self) -> None:
        super().__init__(AlbionActions, NavigatorVision)

    def manage_state(self):
        # Update character info on map

        if self.state == State.START:
            # Move character from node to node
            # save node history
            pass
        else:
            sleep(0.2)
