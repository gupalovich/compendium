from dataclasses import dataclass

import numpy as np


class ValueObject:
    """A base class for all value objects"""


@dataclass(frozen=True)
class Coord(ValueObject):
    """A 2D coordinate

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
        top_left: Coord - the top left corner of the rectangle
        bottom_right: Coord - the bottom right corner of the rectangle
        width: the width property of the rectangle
        height: the height property of the rectangle
    """

    top_left: Coord
    bottom_right: Coord

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

    def center(self) -> Coord:
        """Returns the middle point of the rectangle"""
        x = (self.top_left.x + self.bottom_right.x) / 2
        y = (self.top_left.y + self.bottom_right.y) / 2
        return Coord(x, y)


@dataclass(frozen=True)
class Polygon(ValueObject):
    points: list[Coord]

    def __post_init__(self):
        if len(self.points) < 4:
            raise ValueError("Polygon must have at least 4 points")

    def as_np_array(self) -> np.ndarray:
        """Converts the polygon to a NumPy array of points"""
        return np.array([(point.x, point.y) for point in self.points])


@dataclass(frozen=True)
class Img:
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
        if isinstance(other, Img):
            return (
                np.array_equal(self.img, other.img)
                and self.width == other.width
                and self.height == other.height
            )
        return False


@dataclass(frozen=True)
class MatchLocation:
    """A location and confidence

    Attributes:
        top_left: Coord - the top left corner of the rectangle
        width: the width of search template
        height: the height of search template
        confidence: the confidence threshold
    """

    top_left: Coord
    width: int
    height: int
    confidence: float

    def as_rect(self) -> Rect:
        """Convert match location to a Rect"""
        return Rect(
            top_left=self.top_left,
            bottom_right=Coord(
                x=self.top_left.x + self.width,
                y=self.top_left.y + self.height,
            ),
        )
