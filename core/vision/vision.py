from typing import List

import cv2 as cv
import numpy as np
import pytesseract

from core.common.entities import Coord, DetectedObjects, Img, Rect, RefPath
from core.display.window import WindowHandler
from core.vision.utils import load_img

from .enums import ColorFormat
from .utils import convert_img_color, crop_img, draw_rectangles


class BaseVision:
    method = cv.TM_CCOEFF_NORMED
    cropped_areas = {}
    ui_elements = {}

    def match_template(
        self, ref_img: Img, search_img: Img, confidence: float = 0.65
    ) -> List[tuple[int, int]]:
        """cv2 match template based on confidence value"""

        result = cv.matchTemplate(search_img.data, ref_img.data, self.method)
        locations = np.where(result >= confidence)
        locations = list(zip(*locations[::-1]))  # removes empty arrays
        return locations

    def find(self, ref_img: Img, search_img: Img, crop: Rect = None) -> DetectedObjects:
        ref_width = ref_img.width
        ref_height = ref_img.height
        ref_img_gray = convert_img_color(ref_img, ColorFormat.BGR_GRAY)
        search_img_gray = convert_img_color(search_img, ColorFormat.BGR_GRAY)

        if crop:
            search_img_gray = crop_img(search_img_gray, crop)

        locations = self.match_template(
            ref_img_gray, search_img_gray, ref_img.confidence
        )
        mask = np.zeros(search_img_gray.data.shape[:2], dtype=np.uint8)
        result = DetectedObjects(ref_img, search_img)

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

    def find_ui(
        self, ref_img: Img, search_img: Img, crop: Rect = None
    ) -> DetectedObjects:
        result = self.find(ref_img, search_img, crop)
        return result

    def image_to_text(self, search_img: Img, crop: Rect) -> str:
        return pytesseract.image_to_string(crop_img(search_img, crop))

    def live(
        self,
        ref_path: RefPath,
        exit_key: str = "q",
        resize: Coord = Coord(1200, 675),
        crop: Rect = None,
    ) -> None:
        """
        TODO:
        - Add new class for such cases
        - Add fps counter
        - Add object found logger
        """
        window = WindowHandler()
        while True:
            search_img = window.grab()
            result = self.find_ui(ref_path, search_img, crop)
            show_img = draw_rectangles(search_img, result.locations)
            print("Found: ", len(result))
            show_img = cv.resize(show_img.data, tuple(resize))
            cv.imshow("Debug Screen", show_img)
            key = cv.waitKey(1)
            if key == ord(exit_key):
                cv.destroyAllWindows()
                break
