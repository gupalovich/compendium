from time import time
from unittest import TestCase

from core.common.entities import ImgLoader, Node, Pixel, Vector2d

from ..children import Navigator


class NavigatorTests(TestCase):
    def setUp(self) -> None:
        self.navigator = Navigator()
        self.origin = Pixel(1920 / 2, 1080 / 2)
        self.search_img = ImgLoader("albion/tests/7.png")

    def test_load_cluster(self):
        cluster = self.navigator.load_cluster()
        self.assertIsInstance(cluster, ImgLoader)

    def test_load_cluster_nodes(self):
        nodes = self.navigator.load_cluster_nodes()
        self.assertTrue(len(nodes))
        for node in nodes:
            self.assertIsInstance(node, Node)

    def test_extract_minimap(self):
        minimap = self.navigator.extract_minimap(ImgLoader("albion/tests/7.png"))
        self.assertEqual(minimap.width, 90)
        self.assertEqual(minimap.height, 90)

    def test_create_node_vector(self):
        node = self.navigator.nodes[0]
        node_vector = self.navigator.create_node_vector(node, self.origin)
        expected_vector = Vector2d(node.x - self.origin.x, self.origin.y - node.y)
        self.assertIsInstance(node_vector, Vector2d)
        self.assertEqual(node_vector, expected_vector)

    def test_node_vector_to_pixel_direction(self):
        # node, current_pos, expected_result
        cases = [
            (Node(585, 520), Pixel(560, 520), Pixel(1110, 440)),
            (Node(400, 400), Pixel(0, 0), Pixel(1066, 546)),
            (Node(400, 400), Pixel(1920, 1080), Pixel(823, 378)),
        ]

        for node, current_pos, expected_result in cases:
            node_vector = self.navigator.create_node_vector(node, current_pos)
            self.assertEqual(
                self.navigator.node_vector_to_pixel_direction(node_vector),
                expected_result,
            )

    def test_get_closest_node(self):
        self.navigator.nodes = [
            Node(self.origin.x - 100, self.origin.y - 100),
            Node(self.origin.x - 200, self.origin.y - 200),
            Node(self.origin.x - 300, self.origin.y - 300),
        ]
        cases = [  # char_pos, expected_result
            (self.origin, self.navigator.nodes[0]),
            (Pixel(self.origin.x + 100, self.origin.y + 100), self.navigator.nodes[0]),
            (Pixel(self.origin.x - 149, self.origin.y - 149), self.navigator.nodes[0]),
            (Pixel(self.origin.x - 150, self.origin.y - 150), self.navigator.nodes[1]),
            (Pixel(self.origin.x - 249, self.origin.y - 249), self.navigator.nodes[1]),
            (Pixel(self.origin.x - 250, self.origin.y - 250), self.navigator.nodes[2]),
        ]
        for char_pos, expected_result in cases:
            self.assertEqual(
                self.navigator.get_closest_node(char_pos),
                expected_result,
            )

    def test_find_character_on_map(self):
        self.navigator.search_img = self.search_img
        result = self.navigator.find_character_on_map()
        self.assertEqual(result, Pixel(x=619, y=694))

    def test_add_node_cooldown(self):
        self.navigator.add_node_cooldown(self.navigator.nodes[0])
        self.assertEqual(self.navigator.nodes[0].cooldown, time() + 20)
        self.assertEqual(self.navigator.nodes[1].cooldown, 0)

    def test_clear_node_cooldowns(self):
        node = self.navigator.nodes[0]
        node_1 = self.navigator.nodes[1]
        # set cooldowns
        node.update_cooldown(time() - 20)
        node_1.update_cooldown(time() + 20)
        self.assertNotEqual(node.cooldown, 0)
        self.assertNotEqual(node_1.cooldown, 0)
        # test cooldown reset
        self.navigator.clear_node_cooldowns()
        self.assertEqual(node.cooldown, 0)
        self.assertNotEqual(node_1.cooldown, 0)
