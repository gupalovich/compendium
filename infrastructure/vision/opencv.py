import cv2 as cv
import numpy as np

from infrastructure.common.entities import ProcessedImg


class OpenCV:
    def __init__(self, method=cv.TM_CCOEFF_NORMED):
        self.method = method

    def process_img(self, img_path: str, static_path="static/") -> ProcessedImg:
        """cv2 read image and return processed image"""
        img = cv.imread(static_path + img_path, 0)
        w, h = img.shape[::-1]
        return ProcessedImg(img=img, width=w, height=h)

    def match_template(
        self, screen: np.ndarray, tmplt: np.ndarray, thresh=0.65
    ) -> list:
        """cv2 match template and return locations according to threshold"""
        result = cv.matchTemplate(screen, tmplt, self.method)
        locations = np.where(result >= thresh)
        locations = list(zip(*locations[::-1]))  # removes empty arrays
        return locations

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

    def find(
        self, screen: object, needle_img_path: str, threshold=0.65, crop=[]
    ) -> list[list[int]]:
        """Find grayscaled object on screen by given threshold
        crop - screen region crop [x1, y1, x2, y2]"""
        needle_img, needle_w, needle_h = self.process_img(needle_img_path)
        screen_gray = self.cvt_img_gray(screen)

        if crop:
            screen = screen[crop[1] : crop[3], crop[0] : crop[2]]  # y1:y2, x1:x2
            screen_gray = screen_gray[
                crop[1] : crop[3], crop[0] : crop[2]
            ]  # y1:y2, x1:x2

        # find matches
        locations = self.match_template(screen_gray, needle_img, thresh=threshold)
        mask = np.zeros(screen.shape[:2], np.uint8)
        detected_objects = []

        for x, y in locations:
            if mask[y + needle_h // 2, x + needle_w // 2] != 255:
                detected_objects.append([x, y, needle_w, needle_h])
            mask[y : y + needle_h, x : x + needle_w] = 255  # mask out detected object

        if crop:  # recalculate cropped region points
            for i, (x, y, w, h) in enumerate(detected_objects):
                detected_objects[i] = [x + crop[0], y + crop[1], w, h]

        return detected_objects

    def draw_rectangles(self, haystack_img, rectangles):
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
            cv.rectangle(
                haystack_img, top_left, bottom_right, line_color, lineType=line_type
            )

        return haystack_img

    def draw_crosshairs(self, haystack_img, points):
        """given a list of [x, y] positions and a canvas image to draw on
        return an image with all of those click points drawn on as crosshairs"""
        # these colors are actually BGR
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for center_x, center_y in points:
            # draw the center point
            cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img


open_cv = OpenCV()
