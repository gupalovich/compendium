from core.common.bots import BotChild
from core.common.enums import State

from ..actions.mount import MountActions, MountVision


class Mounter(BotChild):
    def __init__(self) -> None:
        super().__init__(MountVision, MountActions)

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
        super().__init__(MountVision, MountActions)

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
        super().__init__(MountVision, MountActions)

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
