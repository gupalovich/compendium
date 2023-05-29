from typing import List

import cv2 as cv
import numpy as np

from infra.common.entities import Coord, DetectedObjects, Img, Rect

from .enums import ColorFormat
from .utils import convert_img_color, crop_img, draw_rectangles


class OpenCV:
    method = cv.TM_CCOEFF_NORMED

    def _recalculate_cropped_locations(
        self, result: DetectedObjects, crop: Rect
    ) -> DetectedObjects:
        """Recalculate the top-left points of detected objects based on the crop rectangle"""
        result.locations = [
            Rect(
                left_top=Coord(
                    location.left_top.x + crop.left_top.x,
                    location.left_top.y + crop.left_top.y,
                ),
                width=location.width,
                height=location.height,
            )
            for location in result.locations
        ]

        return result

    def match_template(
        self, ref_img: Img, search_img: Img, confidence: float = 0.65
    ) -> List[tuple[int, int]]:
        """cv2 match template based on confidence value"""

        result = cv.matchTemplate(search_img.data, ref_img.data, self.method)
        locations = np.where(result >= confidence)
        locations = list(zip(*locations[::-1]))  # removes empty arrays
        return locations

    def find(
        self, ref_img: Img, search_img: Img, confidence: float = 0.65, crop: Rect = None
    ) -> DetectedObjects:
        ref_width = ref_img.width
        ref_height = ref_img.height
        ref_img_gray = convert_img_color(ref_img, ColorFormat.BGR_GRAY)
        search_img_gray = convert_img_color(search_img, ColorFormat.BGR_GRAY)

        if crop:
            search_img_gray = crop_img(search_img_gray, crop)

        locations = self.match_template(
            ref_img_gray, search_img_gray, confidence=confidence
        )
        mask = np.zeros(search_img_gray.data.shape[:2], dtype=np.uint8)
        result = DetectedObjects(ref_img, search_img, confidence)

        if crop:
            crop_left = crop.left_top.x
            crop_top = crop.left_top.y

        for loc_x, loc_y in locations:
            if crop:
                loc_x += crop_left
                loc_y += crop_top

            center_x = loc_x + ref_width // 2
            center_y = loc_y + ref_height // 2

            if mask[center_y, center_x] != 255:
                loc = Rect(
                    left_top=Coord(loc_x, loc_y), width=ref_width, height=ref_height
                )
                result.add(loc)
                # Mask out detected object
                mask[loc_y : loc_y + ref_height, loc_x : loc_x + ref_width] = 255

        if crop:
            result = self._recalculate_cropped_locations(result, crop)

        return result

    def livestream(
        self,
        screen: Img,
        result: DetectedObjects,
        exit_key: str = "q",
        resize: Coord = Coord(1200, 675),
    ) -> None:
        """
        Debug OpenCV screen template matching by adding rectangles

        Example:
            screen = window.grab()
            locations = opencv.match(screen, "template.png", confidence=0.65)
            opencv.debug(screen, locations, exit_key="q")
        """
        screen = draw_rectangles(screen, result.locations)
        screen = cv.resize(screen, tuple(resize))
        cv.imshow("Debug Screen", screen)
        if cv.waitKey(1) == ord(exit_key):
            cv.destroyAllWindows()
