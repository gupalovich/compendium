from core.common.bots import BotChild
from core.common.enums import State

from ..actions.input import GathererActions, MounterActions, NavigatorActions
from ..actions.vision import GathererVision, MounterVision, NavigatorVision


class Mounter(BotChild):
    def __init__(self) -> None:
        super().__init__(MounterActions, MounterVision)

    def manage_state(self):
        if self.state == State.START:
            if self.vision.is_mounting(self.search_img):
                pass
            elif self.vision.is_mounted(self.search_img):
                self.set_state(State.DONE)
            else:
                self.actions.mount()


class Navigator(BotChild):
    def __init__(self) -> None:
        super().__init__(NavigatorActions, NavigatorVision)

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
        super().__init__(GathererActions, GathererVision)

    def manage_state(self):
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
