from dataclasses import dataclass, field
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


@dataclass
class Rect(ValueObject):
    """A 2d rectangle

    Attributes:
        left_top: Coord
        right_bottom: Optional[Coord] = None
        width: Optional[float] = None
        height: Optional[float] = None

    Example:
        Rect(left_top=(0, 0), right_bottom=(100, 100))
        Rect(left_top=(0, 0), width=100, height=100)
    """

    left_top: Coord
    right_bottom: Optional[Coord] = None
    width: Optional[float] = None
    height: Optional[float] = None

    def __post_init__(self):
        if self.right_bottom is None and (self.width is None or self.height is None):
            raise ValueError(
                "Either right_bottom or both width and height must be provided."
            )

        if self.right_bottom is None:
            self.calc_right_bottom()
        if self.right_bottom and (self.width is None or self.height is None):
            self.calc_dimensions()

    def __iter__(self):
        """Allows iteration, unpacking over value object"""
        yield self.left_top
        yield self.right_bottom
        yield self.width
        yield self.height

    @property
    def center(self) -> Coord:
        """Returns the middle point of the rectangle"""
        x = round((self.left_top.x + self.right_bottom.x) / 2)
        y = round((self.left_top.y + self.right_bottom.y) / 2)
        return Coord(x, y)

    def calc_right_bottom(self) -> Coord:
        """The bottom right point of the rectangle"""
        self.right_bottom = Coord(
            self.left_top.x + self.width,
            self.left_top.y + self.height,
        )

    def calc_dimensions(self) -> None:
        """The width and height of the rectangle"""
        self.width = self.right_bottom.x - self.left_top.x
        self.height = self.right_bottom.y - self.left_top.y


@dataclass(frozen=True)
class Polygon(ValueObject):
    points: list[Coord]

    def __post_init__(self):
        if len(self.points) < 4:
            raise ValueError("Polygon must have at least 4 points")

    def as_np_array(self) -> np.array:
        """Converts the polygon to a NumPy array of points"""
        return np.array([(point.x, point.y) for point in self.points])


@dataclass
class Img:
    data: np.ndarray
    width: Optional[int] = None
    height: Optional[int] = None
    channels: Optional[int] = 1

    def __post_init__(self):
        self.calc_dimensions()

    def __iter__(self):
        """Allows iteration, unpacking over value object"""
        yield self.data
        yield self.width
        yield self.height
        yield self.channels

    def calc_dimensions(self) -> None:
        try:
            self.height, self.width, self.channels = self.data.shape
        except ValueError:
            self.height, self.width = self.data.shape[:2]


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
        if len(rgb) == 3:
            r, g, b = rgb
            return cls(r, g, b)
        elif len(rgb) == 4:
            r, g, b, a = rgb
            return cls(r, g, b, a)
        else:
            raise ValueError("Invalid RGB values. Expected a tuple of length 3 or 4.")

    @classmethod
    def from_bgr(cls, bgr: Tuple[int, int, int, Optional[int]]) -> "Color":
        """Create a Color object from BGR values"""
        if len(bgr) == 3:
            b, g, r = bgr
            return cls(r, g, b)
        elif len(bgr) == 4:
            b, g, r, a = bgr
            return cls(r, g, b, a)
        else:
            raise ValueError("Invalid BGR values. Expected a tuple of length 3 or 4.")

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
    """Entity representing a collection of detected locations"""

    ref_img: Img
    search_img: Img
    confidence: float
    locations: Optional[List[Rect]] = field(default_factory=list)

    def size(self) -> int:
        """Returns the number of detected objects"""
        return len(self.locations)

    def add(self, rect: Rect) -> None:
        self.locations.append(rect)

    def remove(self) -> None:
        raise NotImplementedError()
