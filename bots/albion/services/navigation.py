import math
from typing import List

import cv2 as cv

from config import settings
from core.common.entities import Img, ImgLoader, Pixel, Polygon, Rect, Vector2d
from core.display.utils import draw_circles
from core.display.window import WindowHandler
from core.input.actions import move_click


class ImgExtractor:
    """
    Extracts images region from the game window.

    ### Available extractions:
        - map
        - minimap

    ### Example:
        extractor = ImgExtractor() \n
        img = extractor.extract("map", "filename") \n
        img.show()

    ### TODO: tests
    """

    def __init__(self) -> None:
        self.window = WindowHandler()
        self.img_types = {
            "map": (self.map_crop, "albion/maps/{}.png"),
            "minimap": (self.minimap_crop, "albion/temp/{}.png"),
        }

    def map_crop(self) -> Polygon:
        origin = Pixel(962, 585)
        radius = Pixel(560, 420)
        region = Polygon(
            points=[
                Pixel(origin.x - radius.x, origin.y),
                Pixel(origin.x, origin.y - radius.y),
                Pixel(origin.x + radius.x, origin.y),
                Pixel(origin.x, origin.y + radius.y),
            ]
        )
        return region

    def minimap_crop(self) -> Rect:
        origin = Pixel(1714, 916)
        radius = 65
        region = Rect(
            left_top=Pixel(origin.x - radius, origin.y - radius),
            right_bottom=Pixel(origin.x + radius, origin.y + radius),
        )
        return region

    def extract(self, img_type: str, save_filename: str) -> Img:
        img = self.window.grab()
        crop_func, save_path = self.img_types.get(img_type)
        region = crop_func()

        if isinstance(region, Polygon):
            img.crop_polygon(region)
        else:
            img.crop(region)

        img.save(save_path.format(save_filename))

        return img


class NodeWalker:
    def node_vector(self, char_pos: Pixel, node_pos: Pixel) -> Vector2d:
        return Vector2d(x=node_pos.x - char_pos.x, y=char_pos.y - node_pos.y)

    def node_distance(self, vector: Vector2d) -> float:
        return abs(vector)

    def node_direction(self, vector: Vector2d, distance: float = 150) -> Pixel:
        resolution = Pixel(x=1920, y=1080)
        origin_skew = 100
        origin = Pixel(x=resolution.x / 2, y=resolution.y / 2 - origin_skew)
        radians = vector.angle()
        x = int(origin.x + distance * math.cos(radians))
        y = int(origin.y - distance * math.sin(radians))
        return Pixel(x, y)

    def start(self, char_pos: Pixel, node: Pixel):
        node = self.node_vector(char_pos, node)
        node_dist = self.node_distance(node)
        node_dir = self.node_direction(node)

        print("Node Vector: ", node)
        print("Node Distance: ", node_dist)
        print("Node Direction: ", node_dir, "\n")

        if 2 < node_dist < 50:
            move_click(node_dir)


class NodeMapper:
    """
    Simplify way of mapping nodes to the map

    TODO: NodeMapper based on character position and keybind

    """

    node_color = (255, 255, 0)
    exit_key = "q"

    def __init__(self, map_path: str, nodes: List[Pixel] = None):
        self.map_path = map_path
        self.map = ImgLoader(map_path)
        self.nodes = nodes or []

    def add_node(self, node: Pixel):
        if node in self.nodes:
            return
        self.nodes.append(node)
        print("Added node: ", node)

    def remove_node(self, node: Pixel):
        raise NotImplementedError()

    def save_nodes(self):
        filename = settings.STATIC_PATH + self.map_path.split(".")[0] + "_nodes.txt"
        with open(filename, "w+", encoding="utf-8") as file:
            file.write(str(self.nodes))

    def click_event(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            pixel = Pixel(x, y)
            self.add_node(pixel)

    def start(self):
        while True:
            self.map = draw_circles(self.map, self.nodes, color=self.node_color)
            cv.imshow("NodeMapper Screen", self.map.data)
            cv.setMouseCallback("NodeMapper Screen", self.click_event)
            if cv.waitKey(1) == ord(self.exit_key):
                cv.destroyAllWindows()
                break


# def find_character_on_map():
#     vision = VisionBase()
#     window = WindowHandler()
#     nodes = [
#         Pixel(x=552, y=574),
#         Pixel(x=547, y=584),
#         Pixel(x=543, y=592),
#         Pixel(x=539, y=600),
#         Pixel(x=536, y=610),
#         Pixel(x=526, y=608),
#         Pixel(x=515, y=605),
#         Pixel(x=512, y=592),
#         Pixel(x=516, y=584),
#         Pixel(x=522, y=579),
#         Pixel(x=526, y=573),
#         Pixel(x=528, y=562),
#         Pixel(x=523, y=556),
#         Pixel(x=518, y=545),
#         Pixel(x=512, y=532),
#         Pixel(x=518, y=526),
#         Pixel(x=529, y=528),
#         Pixel(x=536, y=533),
#         Pixel(x=544, y=543),
#         Pixel(x=553, y=548),
#         Pixel(x=558, y=555),
#     ]
#     i = 0
#     while nodes:
#         search_img = ImgLoader("albion/maps/mase_knoll.png")
#         ref_img = window.grab(region=minimap_crop())
#         ref_img.confidence = 0.73
#         ref_img.resize_x(0.71)
#         # ref_img.save("albion/temp/minimap.png")
#         result = vision.find(ref_img, search_img)
#         char_pos = result.locations[0].center

#         # pathing(char_pos, nodes[i])
#         # i += 1

#         search_img = draw_circles(search_img, result.locations)
#         search_img = draw_circles(search_img, nodes, color=(0, 0, 0))
#         search_img.resize(Pixel(1500, 1500))
#         cv.imshow("Debug Screen", search_img.data)
#         key = cv.waitKey(1)
#         if key == ord("q"):
#             cv.destroyAllWindows()
#             break
