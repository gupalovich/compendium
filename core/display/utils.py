import cv2 as cv

from core.common.entities import Img, Pixel, Rect


def draw_rectangles(img: Img, rectangles: list[Rect], with_label=False):
    """Draw rectangles on image in place"""
    bgr = (0, 255, 0)
    thickness = 2

    for rect in rectangles:
        left_top = list(rect.left_top)
        right_bottom = list(rect.right_bottom)
        cv.rectangle(img.data, left_top, right_bottom, bgr, thickness)
        if with_label:
            cv.putText(
                img.data,
                rect.label,
                left_top,
                cv.FONT_HERSHEY_SIMPLEX,
                0.9,
                bgr,
                thickness,
            )
    return img


def draw_crosshairs(img: Img, rectangles: list[Rect]):
    bgr = (255, 0, 255)  # BGR
    marker_type = cv.MARKER_CROSS

    for rect in rectangles:
        center = tuple(rect.center)
        cv.drawMarker(img.data, center, bgr, marker_type)
    return img


def draw_circles(
    img: Img,
    positions: list[Rect | Pixel],
    radius: int = 1,
    thickness: int = 1,
    bgr=(0, 0, 255),
):
    line_type = cv.LINE_4

    for pos in positions:
        if isinstance(pos, Rect):
            pos = tuple(pos.center)
        else:
            pos = tuple(pos)

        cv.circle(img.data, pos, radius, bgr, thickness=thickness, lineType=line_type)
    return img


def draw_lines(img: Img, rectangles: list[Rect]):
    bgr = (0, 0, 255)  # BGR
    thickness = 2

    for rect in rectangles:
        start = list(rect.left_top)
        end = list(rect.right_bottom)
        # Draw the line
        cv.line(img.data, start, end, bgr, thickness=thickness)
    return img
