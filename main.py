import logging

from bots.albion.navigator.extractor import grab_minimap
from config import settings


def main():
    # crop = Rect(Coord(100, 100), Coord(800, 800))
    # BaseVision.live_stream("tests/maps/minimap.png")
    grab_minimap()


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
        )
        logging.info("DEBUG")

    main()
