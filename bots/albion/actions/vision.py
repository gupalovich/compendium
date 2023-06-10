import cv2 as cv

from core.common.entities import Coord, Rect, RefPath
from core.vision.vision import BaseVision


class Vision(BaseVision):
    def __init__(self, method=cv.TM_CCOEFF_NORMED) -> None:
        super().__init__(method)
        self.cropped_areas = {
            "skill_panel": Rect(Coord(480, 975), Coord(1475, 1065)),
        }
        self.ui_elements = {
            "mount": RefPath("albion/ui/mount_hp_1.png", 0.85),
        }
