import cv2 as cv

from core.common.entities import ImgLoader, Pixel, Polygon, Rect
from core.display.utils import draw_circles
from core.display.vision import VisionBase
from core.display.window import WindowHandler


def extract_map(filename: str) -> None:
    window = WindowHandler()
    map_center = Pixel(962, 585)
    crop_size = Pixel(560, 420)
    map_crop = Polygon(
        points=[
            Pixel(map_center.x - crop_size.x, map_center.y),
            Pixel(map_center.x, map_center.y - crop_size.y),
            Pixel(map_center.x + crop_size.x, map_center.y),
            Pixel(map_center.x, map_center.y + crop_size.y),
        ]
    )
    search_img = window.grab()
    search_img.crop_polygon(map_crop)
    search_img.save(f"maps/{filename}.png")


def grab_minimap():
    vision = VisionBase()
    char_pos = Pixel(1710, 912)
    crop_size = 65
    window = WindowHandler()
    minimap_crop = Rect(
        left_top=Pixel(char_pos.x - crop_size, char_pos.y - crop_size),
        right_bottom=Pixel(char_pos.x + crop_size, char_pos.y + crop_size),
    )
    search_img = ImgLoader("albion/maps/mase_knoll.png")
    search_img.resize_x(x_factor=1.55)
    # print(minimap_crop.width, minimap_crop.height)
    # cv.imshow("Debug Screen", ref_img.data)
    # cv.waitKey(0)
    # cv.destroyAllWindows()
    while True:
        ref_img = window.grab(region=minimap_crop)
        ref_img.confidence = 0.75
        ref_img.save("albion/temp/minimap.png")
        result = vision.find(ref_img, search_img)
        print("FOUND: ", len(result))
        show_img = draw_circles(search_img, result.locations, radius=2)
        # show_img = cv.resize(show_img.data, [1200, 875])
        cv.imshow("Debug Screen", show_img.data)
        key = cv.waitKey(1)
        if key == ord("q"):
            cv.destroyAllWindows()
            break
