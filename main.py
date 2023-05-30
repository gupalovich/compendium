import logging

import pydirectinput

from config import settings
from infra.common.decorators import measure_fps
from infra.common.entities import Coord, Rect
from infra.devices.display.window import WindowHandler
from infra.devices.vision.opencv import OpenCV
from infra.devices.vision.utils import load_img


def main():
    window = WindowHandler()
    opencv = OpenCV()
    ref_img = load_img("tests/vision/test_template.png")
    while True:
        search_img = window.grab()
        crop = Rect(Coord(100, 100), Coord(800, 800))
        result = opencv.find(ref_img, search_img, crop=crop)
        if len(result):
            print(pydirectinput.position(), result.locations[0].left_top)
        result = OpenCV.live_stream(search_img, result)
        if result == "exit":
            break


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
        )
        logging.info("DEBUG")

    main()
