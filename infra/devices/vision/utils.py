import cv2 as cv
import numpy as np

from config import settings
from infra.common.entities import Img, Polygon, Rect

from .enums import ColorFormat


def load_img(
    img_path: str,
    static_path: str = None,
    fmt: ColorFormat = ColorFormat.BGR,
) -> Img:
    if static_path is None:
        static_path = settings.STATIC_PATH
    path = static_path + img_path
    img = cv.imread(path, fmt)
    if not img.any():
        raise FileNotFoundError(f"File {path} not found")
    return Img(img)


def save_img(img: Img, img_path: str, static_path: str = None) -> None:
    if static_path is None:
        static_path = settings.STATIC_PATH
    cv.imwrite(static_path + img_path, img.data)


def show_img(img: Img, window_name: str = "Window") -> None:
    cv.imshow(window_name, img.data)
    cv.waitKey(0)


def resize_img(img: Img, zoom_factor: float = 2) -> Img:
    """Zoom in/out image by x = zoom_factor"""
    new_img = cv.resize(img.data, None, fx=zoom_factor, fy=zoom_factor)
    return Img(new_img)


def crop_img(img: Img, region: Rect) -> Img:
    """Crop out rectangle from image"""
    new_img = img.data[
        region.top_left.y : region.bottom_right.y,
        region.top_left.x : region.bottom_right.x,
    ]
    return Img(new_img)


def crop_polygon_img(img: Img, region: Polygon) -> Img:
    """Crop out polygon from image and fill background"""
    points = region.as_np_array()
    # Create a binary mask with the polygon shape
    mask = np.zeros(img.data.shape[:2], dtype=np.uint8)
    cv.fillPoly(mask, [points], 255)
    # Apply the mask to the image
    masked_img = cv.bitwise_and(img.data, img.data, mask=mask)
    # Crop out the masked region
    cropped_img = masked_img[
        min(points[:, 1]) : max(points[:, 1]), min(points[:, 0]) : max(points[:, 0])
    ]
    return Img(cropped_img)


def convert_img_color(img: Img, fmt: ColorFormat) -> Img:
    """Create new instance with converted color"""
    return Img(cv.cvtColor(img.data, fmt))


def draw_rectangles(img, rectangles: list[Rect]):
    """Draw rectangles on image in place"""
    line_color = (0, 255, 0)  # BGR
    line_type = cv.LINE_4

    for rect in rectangles:
        top_left = list(rect.top_left)
        bottom_right = list(rect.bottom_right)
        cv.rectangle(img.data, top_left, bottom_right, line_color, lineType=line_type)
    return img


def draw_crosshairs(img: Img, rectangles: list[Rect]):
    marker_color = (255, 0, 255)  # BGR
    marker_type = cv.MARKER_CROSS

    for rect in rectangles:
        center = tuple(rect.center)
        cv.drawMarker(img.data, center, marker_color, marker_type)
    return img


def draw_circles(img, rectangles: list[Rect], radius: int = 1):
    circle_color = (255, 0, 0)  # BGR
    line_type = cv.LINE_4

    for rect in rectangles:
        center = list(rect.center)
        cv.circle(img.data, center, radius, circle_color, lineType=line_type)
    return img


def draw_lines(img, rectangles: list[Rect]):
    line_color = (0, 0, 255)  # BGR
    line_thickness = 2

    for rect in rectangles:
        start = list(rect.top_left)
        end = list(rect.bottom_right)
        # Draw the line
        cv.line(img.data, start, end, line_color, thickness=line_thickness)
    return img
