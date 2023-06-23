from time import sleep

from core.common.bots import BotChild
from core.common.enums import State

from ..actions.input import AlbionActions
from ..actions.vision import GathererVision, MounterVision, NavigatorVision


class Mounter(BotChild):
    def __init__(self) -> None:
        super().__init__(AlbionActions, MounterVision)

    def manage_state(self):
        if self.state == State.START:
            if self.vision.is_mounting(self.search_img):
                pass
            elif self.vision.is_mounted(self.search_img):
                self.set_state(State.DONE)
            else:
                self.actions.mount()
        else:
            sleep(0.2)


class Navigator(BotChild):
    def __init__(self) -> None:
        super().__init__(AlbionActions, NavigatorVision)

    def manage_state(self):
        # Update character info on map
        match (self.state):
            case State.IDLE:
                pass
            case State.START:
                # Move character from node to node
                # save node history
                pass
            case State.DONE:
                pass


class Gatherer(BotChild):
    def __init__(self) -> None:
        super().__init__(AlbionActions, GathererVision)

    def update_target(self):
        self.targets = {
            "resources": [],
            "monsters": [],
        }

    def manage_state(self):
        if self.search_img:
            self.targets = self.vision.yolo.find(self.search_img, confidence=0.8)
        # Detect targets
        # update self targets
        match (self.state):
            case State.IDLE:
                pass
            case State.START:
                # If targets monster in nearby radius
                # Kill monster until there's none
                # Else: Do gathering
                if not self.targets:
                    self.set_state(State.DONE)
            case State.DONE:
                pass
