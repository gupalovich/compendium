import math
from time import sleep, time
from typing import List

import cv2 as cv

from config import settings
from core.common.entities import Img, ImgLoader, Pixel, Polygon, Rect, Vector2d
from core.display.utils import draw_circles
from core.display.vision import VisionBase
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
        origin = Pixel(1710, 910)
        radius = 65
        region = Rect(
            left_top=Pixel(origin.x - radius, origin.y - radius),
            right_bottom=Pixel(origin.x + radius, origin.y + radius),
        )
        return region

    def extract(self, img_type: str, save_filename: str = "") -> Img:
        save_filename = save_filename or img_type
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
    def __init__(self):
        self.nodes = [
            Pixel(x=585, y=521),
            Pixel(x=586, y=510),
            Pixel(x=590, y=501),
            Pixel(x=601, y=501),
            Pixel(x=610, y=505),
            Pixel(x=619, y=508),
            Pixel(x=629, y=506),
            Pixel(x=619, y=515),
            Pixel(x=613, y=520),
            Pixel(x=611, y=526),
            Pixel(x=604, y=526),
            Pixel(x=596, y=526),
            Pixel(x=590, y=525),
        ]
        self.cooldowns = {}

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

    def get_closest_node_index(self, char_pos: Pixel) -> int:
        closest_distance = float("inf")
        closest_index = None
        for i, node in enumerate(self.nodes):
            node_vector = self.node_vector(char_pos, node)
            node_dist = self.node_distance(node_vector)
            if node_dist < closest_distance:
                closest_distance = node_dist
                closest_index = i
        return closest_index

    def start(self):
        vision = VisionBase()
        extractor = ImgExtractor()
        search_img = ImgLoader("albion/maps/mase_knoll.png")

        while self.nodes:
            search_img.reset()

            ref_img = extractor.extract("minimap")
            ref_img.confidence = 0.72
            ref_img.resize_x(0.69)

            result = vision.find(ref_img, search_img)

            if not result.count:
                sleep(0.1)
                continue

            search_img = draw_circles(search_img, result.locations)
            search_img = draw_circles(search_img, self.nodes, color=(255, 255, 0))
            search_img = draw_circles(search_img, self.cooldowns, color=(0, 0, 0))

            search_img.resize_x(1.2)

            cv.imshow("Debug Screen", search_img.data)
            key = cv.waitKey(1)
            if key == ord("q"):
                cv.destroyAllWindows()
                break

            char_pos = result.locations[0].center

            available_nodes = [
                node for node in self.nodes if node not in self.cooldowns
            ]
            if self.cooldowns:
                current_time = time()
                # Update cooldowns and remove expired ones
                self.cooldowns = {
                    node: cooldown_time
                    for node, cooldown_time in self.cooldowns.items()
                    if cooldown_time > current_time
                }

            closest_index = self.get_closest_node_index(char_pos)
            node = self.nodes[closest_index]
            node_vector = self.node_vector(char_pos, node)
            node_dist = self.node_distance(node_vector)
            node_dir = self.node_direction(node_vector)

            print("Node: ", node)
            print("Node Vector: ", node_vector)
            print("Node Distance: ", node_dist)
            print("Node Direction: ", node_dir, "\n")

            if 2 < node_dist < 50:
                move_click(node_dir)
                # Set the cooldown for the node (e.g., 5 seconds)
                cooldown_time = time() + 5
                self.cooldowns[node] = cooldown_time
            if node_dist < 2:
                self.nodes.remove(node)


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

    def click_event(self, event, x, y, *args):
        # pylint: disable=unused-argument
        if event == cv.EVENT_LBUTTONDOWN:
            pixel = Pixel(x, y)
            self.add_node(pixel)

    def start(self):
        while True:
            self.map = draw_circles(self.map, self.nodes, color=self.node_color)
            cv.imshow("NodeMapper Screen", self.map.data)
            cv.setMouseCallback("NodeMapper Screen", self.click_event)
            if cv.waitKey(1) == ord(self.exit_key):
                print(self.nodes)
                cv.destroyAllWindows()
                break
