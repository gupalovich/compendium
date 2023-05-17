from dataclasses import dataclass

import numpy as np


class ValueObject:
    """A base class for all value objects"""


@dataclass(frozen=True)
class Location(ValueObject):
    """A 2D location

    Attributes:
        x: the x coordinate
        y: the y coordinate
    """

    x: float
    y: float

    def as_tuple(self) -> tuple[float, float]:
        """Return the location as a tuple (x, y)"""
        return (self.x, self.y)


@dataclass(frozen=True)
class Rect(ValueObject):
    """A 2D rectangle

    Attributes:
        top_left: Location - the top left corner of the rectangle
        bottom_right: Location - the bottom right corner of the rectangle
    """

    top_left: Location
    bottom_right: Location

    def middle_point(self) -> Location:
        """Returns the middle point of the rectangle"""
        x = (self.top_left.x + self.bottom_right.x) / 2
        y = (self.top_left.y + self.bottom_right.y) / 2
        return Location(x, y)

    def as_tuple(self) -> tuple[int, int, int, int]:
        """Returns the rectangle as a tuple (top_left, bottom_right)"""
        return (
            self.top_left.x,
            self.top_left.y,
            self.bottom_right.x,
            self.bottom_right.y,
        )


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

    def as_tuple(self) -> tuple[np.ndarray, int, int]:
        """Returns the image as a tuple (img, width, height)"""
        return (self.img, self.width, self.height)


@dataclass(frozen=True)
class MatchLocationInfo:
    """A location and confidence

    Attributes:
        top_left: Location - the top left corner of the rectangle
        width: the width of search template
        height: the height of search template
        confidence: the confidence
    """

    top_left: Location
    width: int
    height: int
    confidence: float

    def as_rect(self) -> Rect:
        """Convert match location to a Rect"""
        return Rect(
            top_left=self.top_left,
            bottom_right=Location(
                x=self.top_left.x + self.width,
                y=self.top_left.y + self.height,
            ),
        )
