from enum import Enum

import cv2 as cv


class ColorFormat(Enum):
    """Enum for

    Attributes:
        BGR: BGR color format
        GRAY: Gray color format
        UNCHANGED: Unchanged color format

        BGR_RGB: BGR to RGB color format
        BGR_GRAY: BGR to Gray color format
        BGR_HSV: BGR to HSV color format
    """

    BGR = cv.IMREAD_COLOR
    GRAY = cv.IMREAD_GRAYSCALE
    UNCHANGED = cv.IMREAD_UNCHANGED
    BGR_RGB = cv.COLOR_BGR2RGB
    BGR_GRAY = cv.COLOR_BGR2GRAY
    BGR_HSV = cv.COLOR_BGR2HSV
