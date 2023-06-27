import math
from time import sleep, time

from core.common.bots import BotChild
from core.common.entities import Img, ImgLoader, Node, Pixel, Rect, Vector2d
from core.common.enums import State
from core.common.utils import find_closest, log
from core.display.vision import YoloVision

from ..actions.input import AlbionActions
from ..actions.utils import extract_minimap
from ..actions.vision import AlbionVision


class Mounter(BotChild):
    def __init__(self) -> None:
        super().__init__()
        self.actions = AlbionActions()
        self.vision = AlbionVision()

    def manage_state(self):
        if self.state == State.START:
            is_mounting = self.vision.is_mounting(self.search_img)
            is_mounted = self.vision.is_mounted(self.search_img)

            if is_mounting:
                log("Mounting", delay=0.3)
            elif is_mounted:
                log("Mounted")
                self.set_state(State.DONE)
            else:
                self.actions.mount()
                log("Trying to mount")
        else:
            sleep(0.2)


class Gatherer(BotChild):
    model_file_path = "ai/albion/models/best_albion1.0.engine"
    classes = [
        "Heretic",
        "Elemental",
        "Sandstone",
        "Rough Stone",
        "Limestone",
        "Birch",
        "Chestnut",
        "Logs",
        "Copper Ore",
        "Tin Ore",
    ]

    def __init__(self) -> None:
        super().__init__()
        self.actions = AlbionActions()
        self.vision = AlbionVision()
        self.yolo = YoloVision(self.model_file_path, self.classes)
        self.targets = {}

    def find_targets(self):
        """Filter out monster/resources from target labels"""

    def get_closest_target(self, locations: list[Rect]):
        origin = Pixel(1920 / 2, 1080 / 2)
        return find_closest(origin, locations)

    def manage_state(self):
        if not self.state:
            return

        self.targets = self.yolo.find(self.search_img, confidence=0.7)

        if self.state == State.START:
            is_gathering = self.vision.is_gathering(self.search_img)

            if self.targets:
                target = self.get_closest_target(self.targets)
                self.actions.gather(target.center)
                log(f"Trying to gather [{target.label}]")
            if is_gathering:
                log("Gathering", delay=0.3)
            if not is_gathering and not self.targets:
                log("Done gathering")
                self.set_state(State.DONE)
        else:
            sleep(0.2)


class Navigator(BotChild):
    clusters = {
        "mase_knoll": {
            "path": "albion/maps/mase_knoll.png",
            "nodes": [
                Node(x=585, y=521),
                Node(x=586, y=510),
                Node(x=590, y=501),
                Node(x=601, y=501),
                Node(x=610, y=505),
                Node(x=619, y=508),
                Node(x=629, y=506),
                Node(x=619, y=515),
                Node(x=613, y=520),
                Node(x=611, y=526),
                Node(x=604, y=526),
                Node(x=596, y=526),
                Node(x=590, y=525),
            ],
        }
    }

    def __init__(self) -> None:
        super().__init__()
        self.actions = AlbionActions()
        self.vision = AlbionVision()
        self.cluster = self.load_cluster()
        self.nodes = self.load_cluster_nodes()
        self.current_node = None

    def load_cluster(self) -> Img:
        return ImgLoader(self.clusters["mase_knoll"]["path"])

    def load_cluster_nodes(self) -> list[Node]:
        return self.clusters["mase_knoll"]["nodes"]

    def extract_minimap(self, search_img: Img) -> Img:
        ref_img = extract_minimap(search_img)
        ref_img.confidence = 0.72
        ref_img.resize_x(0.69)
        return ref_img

    def create_node_vector(self, node: Node, current_pos: Pixel) -> Vector2d:
        return Vector2d(node.x - current_pos.x, current_pos.y - node.y)

    def node_vector_to_pixel_direction(self, node_vector: Vector2d) -> Pixel:
        res_x, res_y = 1920, 1080
        origin_skew = 100
        origin = Pixel(res_x / 2, res_y / 2 - origin_skew)
        radius = 150
        radians = node_vector.angle()
        x = int(origin.x + radius * math.cos(radians))
        y = int(origin.y - radius * math.sin(radians))
        return Pixel(x, y)

    def get_closest_node(self, char_pos: Pixel) -> Node:
        nodes = [node for node in self.nodes if not node.cooldown]
        return find_closest(char_pos, nodes)

    def find_character_on_map(self) -> Pixel:
        """
        TODO: smart way to find character with minimap threshold decrement and multiple results
        """
        minimap = self.extract_minimap(self.search_img)
        result = self.vision.find(minimap, self.cluster)
        return result[0].center

    def add_node_cooldown(self, node: Node, duration: float = 20):
        node.update_cooldown(time() + duration)

    def clear_node_cooldowns(self):
        for node in self.nodes:
            if node.cooldown < time():
                node.reset_cooldown()

    def manage_nodes(self):
        char_location = self.find_character_on_map()  # can't return None
        current_node = self.get_closest_node(char_location)
        node_vector = self.create_node_vector(current_node, char_location)
        node_direction = self.node_vector_to_pixel_direction(node_vector)
        node_distance = abs(node_vector)

        self.clear_node_cooldowns()

        if 2 < node_distance < 50:
            self.actions.move_click(node_direction)
        if node_distance < 2:
            self.add_node_cooldown(current_node)

    def manage_state(self):
        # Update character info on map

        if self.state == State.START:
            # Move character from node to node
            pass
        else:
            sleep(0.2)
