from dataclasses import dataclass

import numpy as np


class ValueObject:
    """A base class for all value objects"""

    def as_tuple(self) -> tuple:
        """Convert the value object to a tuple"""
        return tuple(vars(self).values())


@dataclass(frozen=True)
class Location2D(ValueObject):
    """A 2D location

    Attributes:
        x: the x coordinate
        y: the y coordinate
    """

    x: float
    y: float


@dataclass(frozen=True)
class Rect2D(ValueObject):
    """A 2D rectangle

    Attributes:
        top_left: Location2D - the top left corner of the rectangle
        bottom_right: Location2D - the bottom right corner of the rectangle
    """

    top_left: Location2D
    bottom_right: Location2D

    def middle_point(self) -> Location2D:
        """Returns the middle point of the rectangle"""
        x = (self.top_left.x + self.bottom_right.x) / 2
        y = (self.top_left.y + self.bottom_right.y) / 2
        return Location2D(x, y)


@dataclass(frozen=True)
class ProcessedImg:
    """A processed image

    Attributes:
        img: np.ndarray - the image
        width: int - the width of the image
        height: int - the height of the image
    """

    img: np.ndarray
    width: int
    height: int


@dataclass(frozen=True)
class MatchLocationInfo:
    """A location and confidence

    Attributes:
        x: the x coordinate
        y: the y coordinate
        width: the width of search template
        height: the height of search template
        confidence: the confidence
    """

    top_left: Location2D
    width: int
    height: int
    confidence: float

    def as_rect(self) -> Rect2D:
        """Convert match location to a Rect2D"""
        return Rect2D(
            top_left=self.top_left,
            bottom_right=Location2D(
                x=self.top_left.x + self.width,
                y=self.top_left.y + self.height,
            ),
        )
