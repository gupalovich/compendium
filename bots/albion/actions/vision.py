from core.common.entities import Img, ImgLoader, Pixel, Rect
from core.display.vision import Vision


class AlbionVision(Vision):
    def __init__(self):
        self.crop_areas = {
            "skill_panel": Rect(Pixel(475, 960), Pixel(1480, 1080)),
            "casting": Rect(Pixel(630, 540), Pixel(1255, 780)),
        }
        self.ref_images = {
            "mount_hp": ImgLoader("albion/ui/mount_hp.png", 0.85),
            "skill_teleport": ImgLoader("albion/ui/skill_teleport.png", 0.85),
            "cast_bar": ImgLoader("albion/ui/cast_bar.png", 0.85),
        }

    def _bool_find(self, ref_img_key: str, crop_key: str, search_img: Img) -> bool:
        ref_img = self.ref_images.get(ref_img_key)
        crop = self.crop_areas.get(crop_key)
        result = self.find(ref_img, search_img, crop)
        return bool(result)

    def is_mounting(self, search_img: Img) -> bool:
        return self._bool_find("cast_bar", "casting", search_img)

    def is_mounted(self, search_img: Img) -> bool:
        return self._bool_find("skill_teleport", "skill_panel", search_img)

    def is_gathering(self, search_img: Img) -> bool:
        return self._bool_find("cast_bar", "casting", search_img)
