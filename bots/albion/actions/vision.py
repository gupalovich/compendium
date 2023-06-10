from core.common.entities import Coord, Img, Rect
from core.vision.opencv import OpenCV
from core.vision.utils import load_img

CROPS = {
    "SKILL_PANEL": Rect(Coord(480, 975), Coord(1475, 1065)),
}


def find_mount(search_img: Img):
    ref_img = load_img("albion/ui/mount_hp_1.png")
    result = OpenCV.find(ref_img, search_img, confidence=0.85)
    return result


def find_skill(search_img: Img, ref_name: str):
    skills = {
        "town_teleport": "albion/ui/skill_teleport.png",
    }
    ref_img = load_img(skills[ref_name])
    result = OpenCV.find(
        ref_img, search_img, confidence=0.85, crop=CROPS["SKILL_PANEL"]
    )
    return result
