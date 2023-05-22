import cv2 as cv
import numpy as np

from config import settings
from infra.common.entities import (
    Location,
    MatchLocationInfo,
    Polygon,
    ProcessedImg,
    Rect,
)


class OpenCV:
    def __init__(self, method=cv.TM_CCOEFF_NORMED):
        self.method = method

    def _match_template(
        self, screen: np.ndarray, tmplt: np.ndarray, confidence: float = 0.65
    ) -> tuple:
        """cv2 match template based on confidence value"""

        result = cv.matchTemplate(screen, tmplt, self.method)
        locations = np.where(result >= confidence)
        locations = list(zip(*locations[::-1]))  # removes empty arrays
        return locations

    def _recalculate_cropped_points(
        self, detected_objects: list[MatchLocationInfo], crop: Rect
    ) -> list[MatchLocationInfo]:
        """Recalculate the top-left points of detected objects based on the crop rectangle"""

        recalculated_objects = []

        for match_info in detected_objects:
            x, y = match_info.top_left
            recalculated_top_left = Location(x + crop.top_left.x, y + crop.top_left.y)
            recalculated_objects.append(
                MatchLocationInfo(
                    top_left=recalculated_top_left,
                    width=match_info.width,
                    height=match_info.height,
                    confidence=match_info.confidence,
                )
            )

        return recalculated_objects

    def process_img(self, img_path: str, static_path: str = None) -> ProcessedImg:
        """cv2 read image and return processed image"""
        if static_path is None:
            static_path = settings.STATIC_PATH
        img = cv.imread(static_path + img_path, 0)
        w, h = img.shape[::-1]
        return ProcessedImg(img=img, width=w, height=h)

    def save_img(self, img: np.ndarray, img_path: str, static_path: str = None) -> None:
        """cv2 save image"""
        if static_path is None:
            static_path = settings.STATIC_PATH
        cv.imwrite(static_path + img_path, img)

    def show_img(self, img: np.ndarray, window_name: str = "Window") -> None:
        """cv2 show image"""
        cv.imshow(window_name, img)
        cv.waitKey(0)

    def match(
        self, screen: np.ndarray, tmplt_path: str, confidence=0.65, crop: Rect = None
    ) -> list[MatchLocationInfo]:
        """Find a template in a screen image and return a list of MatchLocationInfo objects"""

        screen = self.cvt_img_color(screen, fmt="bgr")
        screen_gray = self.cvt_img_color(screen, fmt="gray")
        tmplt_img, tmplt_w, tmplt_h = self.process_img(tmplt_path)
        if crop:
            screen = self.crop_img(screen, crop)
            screen_gray = self.crop_img(screen_gray, crop)

        # Find matches
        locations = self._match_template(screen_gray, tmplt_img, confidence=confidence)
        mask = np.zeros(screen.shape[:2], np.uint8)
        detected_objects = []

        for x, y in locations:
            if mask[y + tmplt_h // 2, x + tmplt_w // 2] != 255:
                top_left = Location(x, y)
                detected_objects.append(
                    MatchLocationInfo(
                        top_left=top_left,
                        width=tmplt_w,
                        height=tmplt_h,
                        confidence=confidence,
                    )
                )
            # Mask out detected object
            mask[y : y + tmplt_h, x : x + tmplt_w] = 255

        if crop:
            detected_objects = self._recalculate_cropped_points(detected_objects, crop)

        return detected_objects

    def cvt_img_color(self, img: np.ndarray, fmt: str = "bgr") -> np.ndarray:
        """
        OpenCV convert image color to specific format

        Formats:
            "bgr", "bgra", "rgb", "gray", "hsv"
        """
        formats = {
            "bgr": cv.IMREAD_COLOR,
            "bgra": cv.COLOR_BGRA2BGR,
            "rgb": cv.COLOR_BGRA2RGB,
            "gray": cv.COLOR_BGR2GRAY,
            "hsv": cv.COLOR_BGR2HSV,
        }

        if fmt not in formats:
            raise ValueError(
                f"Invalid format: {fmt}. Supported formats: {formats.keys()}"
            )

        try:
            img = cv.cvtColor(img, formats[fmt])
        except cv.error as e:
            # Handle OpenCV conversion errors
            print(f"Error converting image color: {e}")
            # Optionally, fallback to a default behavior
            img = cv.cvtColor(img, formats["bgr"])

        return img

    def crop_img(self, img: np.ndarray, region: Rect) -> np.ndarray:
        """cv2 crop image according to rect points"""
        img_cropped = img[
            region.top_left.y : region.bottom_right.y,
            region.top_left.x : region.bottom_right.x,
        ]
        return img_cropped

    def crop_polygon(self, img: np.ndarray, region: Polygon) -> np.ndarray:
        """Extract polygon from screen and fill background"""

        points = region.as_np_array()
        # Create a binary mask with the polygon shape
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        cv.fillPoly(mask, [points], 255)
        # Apply the mask to the image
        masked_image = cv.bitwise_and(img, img, mask=mask)
        # Crop out the masked region
        cropped_image = masked_image[
            min(points[:, 1]) : max(points[:, 1]), min(points[:, 0]) : max(points[:, 0])
        ]
        cropped_image = opencv.cvt_img_color(cropped_image, fmt="rgb")
        return cropped_image

    def zoom(self, img: np.ndarray, zoom_factor: float = 2):
        """cv2 resize image with double the size
        # (note: this will not work for images with alpha channel)"""
        return cv.resize(img, None, fx=zoom_factor, fy=zoom_factor)

    def draw_rectangles(self, screen, rectangles: list[MatchLocationInfo]):
        """given a list of [x, y, w, h] rectangles and a canvas image to draw on
        return an image with all of those rectangles drawn"""
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv.LINE_4

        for match_loc in rectangles:
            rect = match_loc.as_rect()
            top_left = list(rect.top_left)
            bottom_right = list(rect.bottom_right)
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
            screen = window.grab()
            locations = opencv.match(screen, "template.png", confidence=0.65)
            opencv.debug(screen, locations, exit_key="q")
        """
        screen = self.draw_rectangles(screen, locations)
        screen = cv.resize(screen, (1200, 675))
        cv.imshow("Debug Screen", screen)
        if cv.waitKey(1) == ord(exit_key):
            cv.destroyAllWindows()


opencv = OpenCV()
