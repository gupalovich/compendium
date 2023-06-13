import logging

from bots.albion.bots.gatherer import Gatherer
from config import settings


def main():
    # crop_areas = {
    #     "skill_panel": Rect(Pixel(480, 975), Pixel(1475, 1065)),
    # }
    # ui_elements = {
    #     "mount": ImgLoader("albion/ui/mount_hp_1.png", 0.9),
    #     "mount_r": ImgLoader("albion/ui/mount_circle_radian.png", 0.87),
    # }

    # # vision_live = VisionLive(ui_elements["mount"], crop_areas["skill_panel"])
    # vision_live = VisionLive(ui_elements["mount"])
    # vision_live.start()

    gatherer = Gatherer()
    gatherer.start()


if __name__ == "__main__":
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s"
        )
        logging.info("DEBUG")

    main()
