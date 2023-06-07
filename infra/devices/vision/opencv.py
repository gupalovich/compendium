from typing import List

import cv2 as cv
import numpy as np

from infra.common.entities import Coord, DetectedObjects, Img, Polygon, Rect
from infra.devices.display.window import WindowHandler
from infra.devices.vision.utils import load_img, resize_img, save_img

from .enums import ColorFormat
from .utils import (
    convert_img_color,
    crop_img,
    crop_polygon_img,
    draw_circles,
    draw_rectangles,
)


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
    def extract_map(cls):
        window = WindowHandler()
        map_center = Coord(962, 585)
        crop_size = Coord(560, 420)
        map_crop = Polygon(
            points=[
                Coord(map_center.x - crop_size.x, map_center.y),
                Coord(map_center.x, map_center.y - crop_size.y),
                Coord(map_center.x + crop_size.x, map_center.y),
                Coord(map_center.x, map_center.y + crop_size.y),
            ]
        )
        search_img = window.grab()
        ref_img = crop_polygon_img(search_img, map_crop)
        save_img(ref_img, "maps/mase_knoll2.png")

    @classmethod
    def grab_minimap(cls):
        """
        1. Load map cluster
        2. Crop screen with minimap region
        3. Resize minimap img
        4. Save minimap img
        5. Find minimap img on screen
        6. Show result
        """
        char_pos = Coord(1710, 912)
        crop_size = 65
        window = WindowHandler()
        minimap_crop = Rect(
            left_top=Coord(char_pos.x - crop_size, char_pos.y - crop_size),
            right_bottom=Coord(char_pos.x + crop_size, char_pos.y + crop_size),
        )
        # print(minimap_crop.width, minimap_crop.height)
        # cv.imshow("Debug Screen", ref_img.data)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        while True:
            search_img = load_img("maps/mase_knoll.png")
            search_img = resize_img(search_img, zoom_factor=1.55)
            ref_img = window.grab(region=minimap_crop)
            save_img(ref_img, "temp/minimap.png")
            result = cls.find(ref_img, search_img, confidence=0.75)
            print("FOUND: ", len(result))
            show_img = draw_circles(search_img, result.locations, radius=2)
            # show_img = cv.resize(show_img.data, [1200, 875])
            cv.imshow("Debug Screen", show_img.data)
            key = cv.waitKey(1)
            if key == ord("q"):
                cv.destroyAllWindows()
                break

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
