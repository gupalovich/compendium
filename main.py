import logging

from config import settings
from infra.devices.vision.opencv import OpenCV
from infra.devices.vision.utils import load_img


def main():
    # crop = Rect(Coord(100, 100), Coord(800, 800))
    # OpenCV.live_stream("tests/maps/minimap.png")
    OpenCV.grab_minimap()


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
        )
        logging.info("DEBUG")

    main()
