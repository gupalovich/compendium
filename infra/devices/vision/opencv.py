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

        for i, location in enumerate(result.locations):
            new_left_top = Coord(
                location.left_top.x + crop.left_top.x,
                location.left_top.y + crop.left_top.y,
            )
            new_location = Rect(
                left_top=new_left_top,
                width=location.width,
                height=location.height,
            )
            result.locations[i] = new_location

        return result

    def _match_template(
        self, ref_img: Img, search_img: Img, confidence: float = 0.65
    ) -> tuple:
        """cv2 match template based on confidence value"""

        result = cv.matchTemplate(search_img, ref_img, self.method)
        locations = np.where(result >= confidence)
        locations = list(zip(*locations[::-1]))  # removes empty arrays
        return locations

    def find(
        self, ref_img: Img, search_img: Img, confidence=0.65, crop: Rect = None
    ) -> DetectedObjects:
        """Find a ref_img in search_img and return DetectedObjects entity"""
        search_img = convert_img_color(search_img, ColorFormat.BGR)
        search_img_gray = convert_img_color(search_img, ColorFormat.BGR_GRAY)
        ref_img, ref_width, ref_height = ref_img

        if crop:
            search_img = crop_img(search_img, crop)
            search_img_gray = crop_img(search_img_gray, crop)

        locations = self._match_template(
            search_img_gray, ref_img, confidence=confidence
        )
        mask = np.zeros(search_img.data.shape[:2], np.uint8)
        result = DetectedObjects(ref_img, search_img, confidence)

        for x, y in locations:
            if mask[y + ref_width // 2, x + ref_height // 2] != 255:
                loc = Rect(left_top=Coord(x, y), width=ref_width, height=ref_height)
                result.add(loc)
            # Mask out detected object
            mask[y : y + ref_height, x : x + ref_width] = 255

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
