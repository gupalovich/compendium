from typing import List

import cv2 as cv
import numpy as np
import pytesseract

from core.common.entities import Img, ImgLoader, Pixel, Rect, SearchResult
from core.common.enums import ColorFormat
from core.display.window import WindowHandler

from .utils import draw_rectangles


class Vision:
    method = cv.TM_CCOEFF_NORMED

    def match_template(
        self, ref_img: Img, search_img: Img, confidence: float = 0.65
    ) -> List[tuple[int, int]]:
        """cv2 match template based on confidence value"""

        result = cv.matchTemplate(search_img.data, ref_img.data, self.method)
        locations = np.where(result >= confidence)
        locations = list(zip(*locations[::-1]))  # removes empty arrays
        return locations

    def find(self, ref_img: Img, search_img: Img, crop: Rect = None) -> SearchResult:
        ref_width, ref_height = ref_img.width, ref_img.height
        ref_img.cvt_color(ColorFormat.BGR_GRAY)
        search_img.cvt_color(ColorFormat.BGR_GRAY)

        if crop:
            search_img.crop(crop)

        locations = self.match_template(ref_img, search_img, ref_img.confidence)
        mask = np.zeros(search_img.data.shape[:2], dtype=np.uint8)
        # reset images for next search
        ref_img.reset()
        search_img.reset()

        result = SearchResult(ref_img, search_img)

        for loc_x, loc_y in locations:
            center_x = loc_x + ref_width // 2
            center_y = loc_y + ref_height // 2

            if mask[center_y, center_x] != 255:
                # Mask out detected object
                mask[loc_y : loc_y + ref_height, loc_x : loc_x + ref_width] = 255

                if crop:
                    loc_x += crop.left_top.x
                    loc_y += crop.left_top.y

                loc = Rect(
                    left_top=Pixel(loc_x, loc_y), width=ref_width, height=ref_height
                )
                result.add(loc)

        return result

    def find_color(self):
        """
        TODO: split into ColorVision, TextVision
        """

    def image_to_text(self, search_img: Img, crop: Rect) -> str:
        search_img.crop(crop)
        return pytesseract.image_to_string(search_img.data)


class VisionLive:
    exit_key = "q"
    to_log = True
    resize = Pixel(1200, 675)

    def __init__(self, ref: ImgLoader, crop: Rect = None):
        self.ref = ref
        self.crop = crop

    def start(self) -> None:
        """
        TODO: Add fps counter
        """
        vision = Vision()
        window = WindowHandler()
        while True:
            search_img = window.grab()
            result = vision.find(self.ref, search_img, self.crop)
            show_img = draw_rectangles(search_img, result.locations)
            show_img.resize(self.resize)
            if self.to_log:
                print("Found objects: ", len(result.locations))
            cv.imshow("Debug Screen", result.search_img.data)
            if cv.waitKey(1) == ord(self.exit_key):
                cv.destroyAllWindows()
                break
