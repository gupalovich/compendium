from core.common.entities import Img, ImgLoader, Pixel, Rect, SearchResult
from core.display.vision import Vision

crop_areas = {
    "skill_panel": Rect(Pixel(475, 960), Pixel(1480, 1080)),
    "casting": Rect(Pixel(630, 540), Pixel(1255, 780)),
}
ref_images = {
    "mount_hp": ImgLoader("albion/ui/mount_hp.png", 0.85),
    "skill_teleport": ImgLoader("albion/ui/skill_teleport.png", 0.85),
    "cast_bar": ImgLoader("albion/ui/cast_bar.png", 0.85),
}


class MounterVision(Vision):
    def find_mount(self, search_img: Img) -> SearchResult:
        pass

    def _check_mount_status(
        self, ref_img_key: str, crop_key: str, search_img: Img
    ) -> bool:
        ref_img = ref_images.get(ref_img_key)
        crop = crop_areas.get(crop_key)
        result = self.find(ref_img, search_img, crop)
        return bool(result)

    def is_mounting(self, search_img: Img) -> bool:
        return self._check_mount_status("cast_bar", "casting", search_img)

    def is_mounted(self, search_img: Img) -> bool:
        return self._check_mount_status("skill_teleport", "skill_panel", search_img)


class NavigatorVision(Vision):
    def locate_character_on_map(self, search_img: Img) -> Pixel:
        pass

    def find_closest_node_to_character(self) -> Pixel:
        pass


class GathererVision(Vision):
    def find_closest(self, result: list[Rect]):
        char_pos = Pixel(1920 / 2, 1080 / 2)

        closest_obj = None
        closest_distance = float("inf")

        for obj in result:
            distance = abs(abs(char_pos) - abs(obj.center))
            if distance < closest_distance:
                closest_distance = distance
                closest_obj = obj

        return closest_obj

    def find_targets(self):
        """Filter out monster/resources from target labels"""

    def is_gathering(self, search_img: Img) -> bool:
        ref_img = ref_images.get("cast_bar")
        crop = crop_areas.get("casting")
        result = self.find(ref_img, search_img, crop)
        return bool(result)
