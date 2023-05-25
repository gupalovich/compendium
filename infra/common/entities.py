from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np


class ValueObject:
    """A base class for all value objects"""


@dataclass(frozen=True)
class Coord(ValueObject):
    """A 2D coordinate

    Attributes:
        x: float
        y: float
    """

    x: float
    y: float

    def __iter__(self):
        """Allows iteration, unpacking over value object"""
        yield self.x
        yield self.y


@dataclass(frozen=True)
class Rect(ValueObject):
    """A 2d rectangle

    Attributes:
        top_left: Coord
        bottom_right: Optional[Coord] = None
        width: Optional[float] = None
        height: Optional[float] = None

    Example:
        Rect(top_left=(0, 0), bottom_right=(100, 100))
        Rect(top_left=(0, 0), width=100, height=100)
    """

    top_left: Coord
    bottom_right: Optional[Coord] = None
    width: Optional[float] = None
    height: Optional[float] = None

    def __post_init__(self):
        if self.bottom_right is None and (self.width is None or self.height is None):
            raise ValueError(
                "Either bottom_right or both width and height must be provided."
            )

        if self.bottom_right is None:
            self.calc_bottom_right()

    def __iter__(self):
        """Allows iteration, unpacking over value object"""
        yield self.top_left.x
        yield self.top_left.y
        yield self.bottom_right.x
        yield self.bottom_right.y

    @property
    def center(self) -> Coord:
        """Returns the middle point of the rectangle"""
        x = (self.top_left.x + self.bottom_right.x) / 2
        y = (self.top_left.y + self.bottom_right.y) / 2
        return Coord(x, y)

    def calc_bottom_right(self) -> Coord:
        """The bottom right point of the rectangle"""
        self.bottom_right = Coord(
            self.top_left.x + self.width,
            self.top_left.y + self.height,
        )


@dataclass(frozen=True)
class Polygon(ValueObject):
    points: list[Coord]

    def __post_init__(self):
        if len(self.points) < 4:
            raise ValueError("Polygon must have at least 4 points")

    def as_np_array(self) -> np.array:
        """Converts the polygon to a NumPy array of points"""
        return np.array([(point.x, point.y) for point in self.points])


@dataclass(frozen=True)
class Img:
    """
    An image object, that will measure width and height on __init__

    Attributes:
        data: np.ndarray - the image
        width: Optional[int]
        height: Optional[int]
    """

    data: np.ndarray
    width: Optional[int]
    height: Optional[int]

    def __init__(self, data: np.ndarray):
        self.data = data
        self.width, self.height = data.shape[::-1]

    def __iter__(self):
        """Allows iteration, unpacking over value object"""
        yield self.data
        yield self.width
        yield self.height


@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int
    a: Optional[int] = None

    def __post_init__(self):
        """Perform additional validates after object initialization"""
        self._validate_color_limits()

    def _validate_color_limits(self):
        """Check if color values exceed the limit of 0-255"""
        if not 0 <= self.r <= 255:
            raise ValueError("Invalid color value for 'r'. Must be between 0 and 255.")
        if not 0 <= self.g <= 255:
            raise ValueError("Invalid color value for 'g'. Must be between 0 and 255.")
        if not 0 <= self.b <= 255:
            raise ValueError("Invalid color value for 'b'. Must be between 0 and 255.")
        if self.a is not None and not 0 <= self.a <= 255:
            raise ValueError("Invalid color value for 'a'. Must be between 0 and 255.")

    @classmethod
    def from_rgb(cls, rgb: Tuple[int, int, int, Optional[int]]) -> "Color":
        """Create a Color object from RGB values"""
        r, g, b, a = rgb
        return cls(r, g, b, a)

    @classmethod
    def from_bgr(cls, bgr: Tuple[int, int, int, Optional[int]]) -> "Color":
        """Create a Color object from BGR values"""
        b, g, r, a = bgr
        return cls(r, g, b, a)

    def to_rgb(self) -> Tuple[int, int, int, Optional[int]]:
        """Return RGB values of the color"""
        if self.a is None:
            return self.r, self.g, self.b
        return self.r, self.g, self.b, self.a

    def to_bgr(self) -> Tuple[int, int, int, Optional[int]]:
        """Return BGR values of the color"""
        if self.a is None:
            return self.b, self.g, self.r
        return self.b, self.g, self.r, self.a


@dataclass
class DetectedObjects:
    """Entity representing a collection of detected objects

    TODO: move to vision module
    """

    ref_img: Img
    search_img: Img
    confidence: float
    locations: Optional[List[Rect]] = []

    def size(self) -> int:
        """Returns the number of detected objects"""
        return len(self.locations)

    def add(self, rect: Rect) -> None:
        self.locations.append(rect)

    def remove(self) -> None:
        raise NotImplementedError()
