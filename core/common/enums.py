from enum import Enum, auto

import cv2 as cv


class ColorFormat:
    """
    BGR: cv.IMREAD_COLOR
    GRAY: cv.IMREAD_GRAYSCALE
    UNCHANGED: cv.IMREAD_UNCHANGED
    BGR_RGB: cv.COLOR_BGR2RGB
    BGR_GRAY: cv.COLOR_BGR2GRAY
    BGR_HSV: cv.COLOR_BGR2HSV
    """

    BGR = cv.IMREAD_COLOR
    GRAY = cv.IMREAD_GRAYSCALE
    UNCHANGED = cv.IMREAD_UNCHANGED
    BGR_RGB = cv.COLOR_BGR2RGB
    BGR_GRAY = cv.COLOR_BGR2GRAY
    BGR_HSV = cv.COLOR_BGR2HSV


class State(Enum):
    """Enum states for Bot instances

    #### Available states:
        :param INITIAL = 0
        :param STARTED = auto()
        :param STOPPED = auto()
    """

    INIT = 0
    SEARCHING = auto()
    MOUNTING = auto()
    GATHERING = auto()
    KILLING = auto()
    # Status
    IDLE = 0
    READY = auto()
    DONE = auto()
    FAILED = auto()
