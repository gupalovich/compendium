from typing import List

import cv2 as cv
import numpy as np

from core.common.entities import Coord, DetectedObjects, Img, Rect
from core.display.window import WindowHandler

from .enums import ColorFormat
from .utils import convert_img_color, crop_img, draw_rectangles


class OpenCV:
    method = cv.TM_CCOEFF_NORMED

    @classmethod
    def match_template(
        cls, ref_img: Img, search_img: Img, confidence: float = 0.65
    ) -> List[tuple[int, int]]:
        """cv2 match template based on confidence value"""

        result = cv.matchTemplate(search_img.data, ref_img.data, cls.method)
        locations = np.where(result >= confidence)
        locations = list(zip(*locations[::-1]))  # removes empty arrays
        return locations

    @classmethod
    def find(
        cls, ref_img: Img, search_img: Img, confidence: float = 0.65, crop: Rect = None
    ) -> DetectedObjects:
        ref_width = ref_img.width
        ref_height = ref_img.height
        ref_img_gray = convert_img_color(ref_img, ColorFormat.BGR_GRAY)
        search_img_gray = convert_img_color(search_img, ColorFormat.BGR_GRAY)

        if crop:
            search_img_gray = crop_img(search_img_gray, crop)

        locations = cls.match_template(
            ref_img_gray, search_img_gray, confidence=confidence
        )
        mask = np.zeros(search_img_gray.data.shape[:2], dtype=np.uint8)
        result = DetectedObjects(ref_img, search_img, confidence)

        for loc_x, loc_y in locations:
            if crop:
                loc_x += crop.left_top.x
                loc_y += crop.left_top.y

            center_x = loc_x + ref_width // 2
            center_y = loc_y + ref_height // 2

            if mask[center_y, center_x] != 255:
                loc = Rect(
                    left_top=Coord(loc_x, loc_y), width=ref_width, height=ref_height
                )
                result.add(loc)
                # Mask out detected object
                mask[loc_y : loc_y + ref_height, loc_x : loc_x + ref_width] = 255

        return result

    @classmethod
    def live_stream(
        cls,
        ref_img: Img,
        exit_key: str = "q",
        resize: Coord = Coord(1200, 675),
        crop: Rect = None,
    ) -> None:
        """
        TODO:
        - Add fps counter
        - Add object found logger
        """
        window = WindowHandler()
        while True:
            search_img = window.grab()
            result = cls.find(ref_img, search_img, crop=crop)
            show_img = draw_rectangles(search_img, result.locations)
            show_img = cv.resize(show_img.data, tuple(resize))
            cv.imshow("Debug Screen", show_img)
            key = cv.waitKey(1)
            if key == ord(exit_key):
                cv.destroyAllWindows()
                break
