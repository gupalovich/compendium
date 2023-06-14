from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import cv2 as cv
import numpy as np

from config import settings

from .enums import ColorFormat


class ValueObject:
    """A base class for all value objects"""


@dataclass(frozen=True)
class Pixel:
    """A 2D pixel coordinate

    #### Attributes:
        :x: int
        :y: int
    """

    x: int
    y: int

    def __iter__(self):
        return (i for i in (self.x, self.y))


@dataclass
class Rect:
    """A 2d rectangle

    #### Attributes:
        :left_top: Pixel
        :right_bottom: Optional[Pixel] = None
        :width: Optional[float] = None
        :height: Optional[float] = None

    #### Example:
        - Rect(left_top=Pixel(0, 0), right_bottom=Pixel(100, 100))
        - Rect(left_top=Pixel(0, 0), width=100, height=100)
    """

    left_top: Pixel
    right_bottom: Optional[Pixel] = None
    width: Optional[int] = None
    height: Optional[int] = None

    def __post_init__(self):
        if self.right_bottom is None and (self.width is None or self.height is None):
            raise ValueError(
                "Either right_bottom or both width and height must be provided."
            )

        if self.right_bottom is None:
            self._calc_right_bottom()
        if self.right_bottom and (self.width is None or self.height is None):
            self._calc_dimensions()

    def __iter__(self):
        return (i for i in (self.left_top, self.right_bottom, self.width, self.height))

    @property
    def center(self) -> Pixel:
        """Returns the middle point of the rectangle"""
        x = round((self.left_top.x + self.right_bottom.x) / 2)
        y = round((self.left_top.y + self.right_bottom.y) / 2)
        return Pixel(x, y)

    def _calc_right_bottom(self) -> Pixel:
        """The bottom right point of the rectangle"""
        self.right_bottom = Pixel(
            self.left_top.x + self.width,
            self.left_top.y + self.height,
        )

    def _calc_dimensions(self) -> None:
        """The width and height of the rectangle"""
        self.width = self.right_bottom.x - self.left_top.x
        self.height = self.right_bottom.y - self.left_top.y


@dataclass(frozen=True)
class Polygon(ValueObject):
    """A 2d polygon

    #### Attributes:
        points: list[Pixel]
    """

    points: list[Pixel]

    def __post_init__(self):
        if len(self.points) < 4:
            raise ValueError("Polygon must have at least 4 points")

    def as_np_array(self) -> np.array:
        """Converts the polygon to a NumPy array of points"""
        return np.array([(point.x, point.y) for point in self.points])


@dataclass(frozen=True)
class Color(ValueError):
    """A color respresenting value object

    #### Attributes:
        r: int
        g: int
        b: int
        a: Optional[int] = None
    """

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


class ImgBase:
    _data: Optional[np.ndarray] = None
    data: Optional[np.ndarray] = None
    path: Optional[str] = ""
    confidence: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None
    channels: Optional[int] = 1

    @property
    def initial(self):
        return self._data

    def __iter__(self):
        return (i for i in (self.width, self.height, self.channels))

    def __repr__(self):
        msg = (
            f"<Img(width={self.width}, height={self.height}, channels={self.channels})>"
        )
        return msg

    def _set_params(self) -> None:
        self.data = self.initial
        self._set_dimensions()

    def _set_dimensions(self):
        try:
            self.height, self.width, self.channels = self.data.shape
        except ValueError:
            self.height, self.width = self.data.shape[:2]
            self.channels = 1

    def reset(self):
        self.data = self.initial
        self._set_dimensions()

    def save(self, img_path: str) -> None:
        cv.imwrite(settings.STATIC_PATH + img_path, self.data)

    def crop(self, region: Rect) -> None:
        self.data = self.data[
            region.left_top.y : region.right_bottom.y,
            region.left_top.x : region.right_bottom.x,
        ]
        self._set_dimensions()

    def crop_polygon(self, region: Polygon) -> None:
        """Crop out polygon from image and fill background"""
        points = region.as_np_array()
        # Create a binary mask with the polygon shape
        mask = np.zeros((self.height, self.width), dtype=np.uint8)
        cv.fillPoly(mask, [points], 255)
        # Apply the mask to the image
        masked_img = cv.bitwise_and(self.data, self.data, mask=mask)
        # Crop out the masked region
        self.data = masked_img[
            min(points[:, 1]) : max(points[:, 1]), min(points[:, 0]) : max(points[:, 0])
        ]
        self._set_dimensions()

    def resize(self, size: Pixel) -> None:
        self.data = cv.resize(self.data, tuple(size))
        self._set_dimensions()

    def resize_x(self, x_factor: float = 2) -> None:
        self.data = cv.resize(self.data, None, fx=x_factor, fy=x_factor)
        self._set_dimensions()

    def cvt_color(self, fmt: ColorFormat) -> None:
        self.data = cv.cvtColor(self.data, fmt)
        self._set_dimensions()

    def show(self, window_name: str = "Window") -> None:
        cv.imshow(window_name, self.data)
        cv.waitKey(0)


class Img(ImgBase):
    """Use if you already have an image"""

    def __init__(self, data: str) -> None:
        self._data = data
        self._set_params()


class ImgLoader(ImgBase):
    """Use if you don't have an image"""

    def __init__(self, path: str, conf=0.65, fmt=ColorFormat.BGR) -> None:
        self.path = path
        self.confidence = conf
        self.fmt = fmt
        self._load()
        self._set_params()

    def _load(self) -> None:
        img = cv.imread(settings.STATIC_PATH + self.path, self.fmt)
        if not img.any():
            raise FileNotFoundError(f"Img {self.path} not found")
        self._data = img


@dataclass
class SearchResult:
    """Entity representing a collection of detected locations

    #### Attributes:
        :ref_img: Img
        :search_img: Img
        :locations: Optional[List[Rect]]
    """

    ref_img: Img
    search_img: Img
    locations: Optional[List[Rect]] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.locations)

    def __iter__(self):
        yield self.locations

    def add(self, rect: Rect) -> None:
        self.locations.append(rect)

    def remove(self) -> None:
        raise NotImplementedError()


@dataclass
class Action:
    """
    TODO
    """

    func: callable
    args: tuple
    result: SearchResult

    def __repr__(self) -> str:
        return f"<Action(func={self.func}, args={self.args}, result={self.result})>"


class Task:
    """Entity representing a bot task"""

    """
    TODO
    """

    def __init__(self, name: str, nodes: List[Action]) -> None:
        self.name = name
        self.nodes = enumerate(nodes)
        self.current_node = None

    def __repr__(self) -> str:
        return f"<Task(name={self.name}, current_node={self.current_node}>"

    def __iter__(self):
        yield self.nodes
