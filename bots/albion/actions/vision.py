from core.common.entities import ImgLoader, Pixel, Rect
from core.display.vision import VisionBase


class Vision(VisionBase):
    def __init__(self) -> None:
        self.crop_areas = {
            "skill_panel": Rect(Pixel(480, 975), Pixel(1475, 1065)),
        }
        self.ui_elements = {
            "mount": ImgLoader("albion/ui/mount_hp.png", 0.95),
        }
