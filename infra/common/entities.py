from dataclasses import dataclass

import numpy as np


class ValueObject:
    """A base class for all value objects"""


@dataclass(frozen=True)
class Location(ValueObject):
    """A 2D location

    Attributes:
        x: the x point
        y: the y point
    """

    x: float
    y: float

    def __iter__(self):
        """Allows iteration, unpacking over value object"""
        yield self.x
        yield self.y


@dataclass(frozen=True)
class Rect(ValueObject):
    """A 2D rectangle

    Attributes:
        top_left: Location - the top left corner of the rectangle
        bottom_right: Location - the bottom right corner of the rectangle
        width: the width property of the rectangle
        height: the height property of the rectangle
    """

    top_left: Location
    bottom_right: Location

    def __iter__(self):
        """Allows iteration, unpacking over value object"""
        yield self.top_left.x
        yield self.top_left.y
        yield self.bottom_right.x
        yield self.bottom_right.y

    @property
    def width(self) -> float:
        """The width of the rectangle"""
        return self.bottom_right.x - self.top_left.x

    @property
    def height(self) -> float:
        """The height of the rectangle"""
        return self.bottom_right.y - self.top_left.y

    def center(self) -> Location:
        """Returns the middle point of the rectangle"""
        x = (self.top_left.x + self.bottom_right.x) / 2
        y = (self.top_left.y + self.bottom_right.y) / 2
        return Location(x, y)


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

    def __iter__(self):
        """Allows iteration, unpacking over value object"""
        yield self.img
        yield self.width
        yield self.height

    def __eq__(self, other):
        """Compares two processed images"""
        if isinstance(other, ProcessedImg):
            return (
                np.array_equal(self.img, other.img)
                and self.width == other.width
                and self.height == other.height
            )
        return False


@dataclass(frozen=True)
class MatchLocationInfo:
    """A location and confidence

    Attributes:
        top_left: Location - the top left corner of the rectangle
        width: the width of search template
        height: the height of search template
        confidence: the confidence threshold
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
