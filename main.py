import logging

from config import settings
from infra.common.entities import Coord, Rect
from infra.devices.vision.opencv import OpenCV
from infra.devices.vision.utils import load_img


def main():
    ref_img = load_img("tests/vision/test_template.png")
    # crop = Rect(Coord(100, 100), Coord(800, 800))
    OpenCV.live_stream(ref_img)


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
        )
        logging.info("DEBUG")

    main()
