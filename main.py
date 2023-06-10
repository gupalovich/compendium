import logging

from bots.albion.actions.vision import Vision
from config import settings


def main():
    vision = Vision()
    ref_path = vision.ui_elements["mount"]
    vision.live(ref_path)


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
        )
        logging.info("DEBUG")

    main()
