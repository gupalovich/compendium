import cv2 as cv

from core.common.entities import Coord, Polygon, Rect
from core.display.window import WindowHandler
from core.vision.utils import (
    crop_polygon_img,
    draw_circles,
    load_img,
    resize_img,
    save_img,
)
from core.vision.vision import BaseVision


def extract_map(filename: str) -> None:
    window = WindowHandler()
    map_center = Coord(962, 585)
    crop_size = Coord(560, 420)
    map_crop = Polygon(
        points=[
            Coord(map_center.x - crop_size.x, map_center.y),
            Coord(map_center.x, map_center.y - crop_size.y),
            Coord(map_center.x + crop_size.x, map_center.y),
            Coord(map_center.x, map_center.y + crop_size.y),
        ]
    )
    search_img = window.grab()
    ref_img = crop_polygon_img(search_img, map_crop)
    save_img(ref_img, f"maps/{filename}.png")


def grab_minimap():
    char_pos = Coord(1710, 912)
    crop_size = 65
    window = WindowHandler()
    minimap_crop = Rect(
        left_top=Coord(char_pos.x - crop_size, char_pos.y - crop_size),
        right_bottom=Coord(char_pos.x + crop_size, char_pos.y + crop_size),
    )
    # print(minimap_crop.width, minimap_crop.height)
    # cv.imshow("Debug Screen", ref_img.data)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    while True:
        search_img = load_img("albion/maps/mase_knoll.png")
        search_img = resize_img(search_img, zoom_factor=1.55)
        ref_img = window.grab(region=minimap_crop)
        save_img(ref_img, "albion/temp/minimap.png")
        result = BaseVision.find(ref_img, search_img, confidence=0.75)
        print("FOUND: ", len(result))
        show_img = draw_circles(search_img, result.locations, radius=2)
        # show_img = cv.resize(show_img.data, [1200, 875])
        cv.imshow("Debug Screen", show_img.data)
        key = cv.waitKey(1)
        if key == ord("q"):
            cv.destroyAllWindows()
            break
