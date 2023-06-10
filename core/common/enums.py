from enum import Enum, auto


class State(Enum):
    """Enum states for bot instances

    #### Available states:
        :param INITIAL = 0
        :param STARTED = auto()
        :param STOPPED = auto()
    """

    INITIAL = 0
    STARTED = auto()
    STOPPED = auto()
    # Actions
    MOVING = auto()
    GATHERING = auto()
    SEARCHING = auto()
