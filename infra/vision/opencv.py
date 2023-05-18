import cv2 as cv
import numpy as np

from infra.common.entities import Location, MatchLocationInfo, ProcessedImg, Rect


class OpenCV:
    def __init__(self, method=cv.TM_CCOEFF_NORMED):
        self.method = method

    def process_img(self, img_path: str, static_path="static/") -> ProcessedImg:
        """cv2 read image and return processed image"""
        img = cv.imread(static_path + img_path, 0)
        w, h = img.shape[::-1]
        return ProcessedImg(img=img, width=w, height=h)

    def _match_template(
        self, screen: np.ndarray, tmplt: np.ndarray, confidence=0.65
    ) -> list:
        """cv2 match template based on confidence value"""

        result = cv.matchTemplate(screen, tmplt, self.method)
        locations = np.where(result >= confidence)
        locations = list(zip(*locations[::-1]))  # removes empty arrays
        return locations

    def match(
        self, screen: np.ndarray, tmplt_path: str, confidence=0.65, crop: Rect = None
    ) -> list[MatchLocationInfo]:
        """Find a template in a screen image and return a list of MatchLocationInfo objects"""

        needle_img, needle_w, needle_h = self.process_img(tmplt_path)
        screen_gray = self.cvt_img_gray(screen)

        if crop:
            screen = self.crop_img(screen, crop)
            screen_gray = self.crop_img(screen_gray, crop)

        # find matches
        locations = self._match_template(screen_gray, needle_img, confidence=confidence)
        mask = np.zeros(screen.shape[:2], np.uint8)
        detected_objects = []

        for x, y in locations:
            if mask[y + needle_h // 2, x + needle_w // 2] != 255:
                detected_objects.append(
                    MatchLocationInfo(
                        top_left=Location(x, y),
                        width=needle_w,
                        height=needle_h,
                        confidence=confidence,
                    )
                )
            mask[y : y + needle_h, x : x + needle_w] = 255  # mask out detected object

        if crop:  # recalculate cropped region points
            for i, (x, y, w, h) in enumerate(detected_objects):
                detected_objects[i] = [x + crop[0], y + crop[1], w, h]

        return detected_objects

    def cvt_img_normal(self, img: np.ndarray) -> np.ndarray:
        """cv2 convert image to grayscale format"""
        img_gray = cv.cvtColor(img, cv.IMREAD_COLOR)
        return img_gray

    def cvt_img_gray(self, img: np.ndarray) -> np.ndarray:
        """cv2 convert image to grayscale format"""
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        return img_gray

    def cvt_img_rgb(self, img: np.ndarray) -> np.ndarray:
        """cv2 convert image to rgb format"""
        img_rgb = cv.cvtColor(img, cv.COLOR_BGRA2RGB)
        return img_rgb

    def cvt_img_hsv(self, img: np.ndarray) -> np.ndarray:
        """cv2 convert image to HSV format"""
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        return img_hsv

    def crop_img(self, img: np.ndarray, region: Rect) -> np.ndarray:
        """cv2 crop image according to rect points"""
        img_cropped = img[
            region.top_left.y : region.bottom_right.y,
            region.top_left.x : region.bottom_right.x,
        ]
        return img_cropped

    def draw_rectangles(self, screen, rectangles: list[MatchLocationInfo]):
        """given a list of [x, y, w, h] rectangles and a canvas image to draw on
        return an image with all of those rectangles drawn"""
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for x, y, w, h in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv.rectangle(screen, top_left, bottom_right, line_color, lineType=line_type)

        return screen

    def draw_crosshairs(self, screen, points):
        """given a list of [x, y] positions and a canvas image to draw on
        return an image with all of those click points drawn on as crosshairs"""
        # these colors are actually BGR
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for center_x, center_y in points:
            # draw the center point
            cv.drawMarker(screen, (center_x, center_y), marker_color, marker_type)

        return screen

    def debug(
        self,
        screen: np.ndarray,
        locations: list[MatchLocationInfo],
        exit_key: str = "q",
    ) -> None:
        """
        Debug OpenCV screen template matching by adding rectangles

        Example:
            screen = screen.grab()
            locations = opencv.match(screen, "template.png", confidence=0.65)
            opencv.debug(screen, locations, exit_key="q")
        """

        screen = self.draw_rectangles(screen, locations)
        screen = cv.resize(screen, (1200, 675))
        cv.imshow("Debug Screen", screen)
        if cv.waitKey(1) == ord(exit_key):
            cv.destroyAllWindows()


opencv = OpenCV()
