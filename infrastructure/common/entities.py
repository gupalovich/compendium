from dataclasses import dataclass

import numpy as np


class ValueObject:
    """A base class for all value objects"""


@dataclass(frozen=True)
class Location2D(ValueObject):
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
class Rect2D(ValueObject):
    """A 2D rectangle

    Attributes:
        top_left: Location2D - the top left corner of the rectangle
        bottom_right: Location2D - the bottom right corner of the rectangle
    """

    top_left: Location2D
    bottom_right: Location2D

    def contains(self, location: Location2D) -> bool:
        """Returns true if the location is contained in the rectangle"""
        return (
            location.x >= self.top_left.x
            and location.x <= self.bottom_right.x
            and location.y >= self.top_left.y
            and location.y <= self.bottom_right.y
        )

    def middle_point(self) -> Location2D:
        """Returns the middle point of the rectangle"""
        x = (self.top_left.x + self.bottom_right.x) / 2
        y = (self.top_left.y + self.bottom_right.y) / 2
        return Location2D(x, y)


@dataclass(frozen=True)
class Crop2D(ValueObject):
    """A crop of an image

    Attributes:
        top_left: Location2D - the top left corner of the crop
        width: float - the width of the crop
        height: float - the height of the crop
    """

    top_left: Location2D
    width: float
    height: float

    def as_rect(self) -> Rect2D:
        """Returns the crop as a rect"""
        return Rect2D(
            top_left=self.top_left,
            bottom_right=Location2D(
                x=self.top_left.x + self.width,
                y=self.top_left.y + self.height,
            ),
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
