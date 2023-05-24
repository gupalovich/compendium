import cv2 as cv
import numpy as np

from config import settings
from infra.common.entities import Coord, DetectedObjects, Img, Rect


class OpenCV:
    method = cv.TM_CCOEFF_NORMED

    def _recalculate_cropped_points(
        self, results: DetectedObjects, crop: Rect
    ) -> DetectedObjects:
        """Recalculate the top-left points of detected objects based on the crop rectangle"""

        recalculated_objects = []

        for match_info in detected_objects:
            x, y = match_info.top_left
            recalculated_top_left = Coord(x + crop.top_left.x, y + crop.top_left.y)
            recalculated_objects.append(
                MatchLocation(
                    rect=Rect(
                        top_left=recalculated_top_left,
                        width=match_info.width,
                        height=match_info.height,
                    ),
                    confidence=match_info.confidence,
                )
            )

        return recalculated_objects

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

    def match(
        self, ref_img: Img, search_img: Img, confidence=0.65, crop: Rect = None
    ) -> DetectedObjects:
        """Find a template in a screen image and return a list of MatchLocation objects"""

        search_img = self.cvt_img_color(search_img, fmt="bgr")
        search_img_gray = self.cvt_img_color(search_img, fmt="gray")
        tmplt_img, tmplt_w, tmplt_h = template
        if crop:
            search_img = self.crop_img(search_img, crop)
            search_img_gray = self.crop_img(search_img_gray, crop)

        # Find matches
        locations = self._match_template(
            search_img_gray, tmplt_img, confidence=confidence
        )
        mask = np.zeros(search_img.shape[:2], np.uint8)
        detected_objects = []

        for x, y in locations:
            if mask[y + tmplt_h // 2, x + tmplt_w // 2] != 255:
                top_left = Coord(x, y)
                # TODO: detected_objects into entity: confidence, img, template, locations
                detected_objects.append(
                    MatchLocation(
                        rect=Rect(
                            top_left=top_left,
                            width=tmplt_w,
                            height=tmplt_h,
                        ),
                        confidence=confidence,
                    )
                )
            # Mask out detected object
            mask[y : y + tmplt_h, x : x + tmplt_w] = 255

        if crop:
            detected_objects = self._recalculate_cropped_points(detected_objects, crop)

        return detected_objects

    def livestream(
        self,
        screen: np.ndarray,
        locations: list[MatchLocation],
        exit_key: str = "q",
    ) -> None:
        """
        Debug OpenCV screen template matching by adding rectangles

        Example:
            screen = window.grab()
            locations = opencv.match(screen, "template.png", confidence=0.65)
            opencv.debug(screen, locations, exit_key="q")
        """
        screen = self.draw_rectangles(screen, locations)
        screen = cv.resize(screen, (1200, 675))
        cv.imshow("Debug Screen", screen)
        if cv.waitKey(1) == ord(exit_key):
            cv.destroyAllWindows()
