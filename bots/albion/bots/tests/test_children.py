from unittest import TestCase

from core.common.entities import ImgLoader, Node, Pixel

from ..children import Navigator


class NavigatorTests(TestCase):
    def setUp(self) -> None:
        self.navigator = Navigator()

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
        self.assertEqual(minimap.confidence, 0.72)
        self.assertEqual(minimap.width, 90)
        self.assertEqual(minimap.height, 90)

    def test_node_to_pixel_direction(self):
        # node, current_pos, expected_result
        cases = [
            (Node(585, 520), Pixel(560, 520), Pixel(1110, 440)),
            (Node(400, 400), Pixel(0, 0), Pixel(1066, 546)),
            (Node(400, 400), Pixel(1920, 1080), Pixel(823, 378)),
        ]

        for node, current_pos, expected_result in cases:
            self.assertEqual(
                self.navigator.node_to_pixel_direction(node, current_pos),
                expected_result,
            )

    def test_get_closest_node(self):
        origin = Pixel(1920 / 2, 1080 / 2)
        self.navigator.nodes = [
            Node(origin.x - 100, origin.y - 100),
            Node(origin.x - 200, origin.y - 200),
            Node(origin.x - 300, origin.y - 300),
        ]
        cases = [  # char_pos, expected_result
            (origin, self.navigator.nodes[0]),
            (Pixel(origin.x + 100, origin.y + 100), self.navigator.nodes[0]),
            (Pixel(origin.x - 149, origin.y - 149), self.navigator.nodes[0]),
            (Pixel(origin.x - 150, origin.y - 150), self.navigator.nodes[1]),
            (Pixel(origin.x - 249, origin.y - 249), self.navigator.nodes[1]),
            (Pixel(origin.x - 250, origin.y - 250), self.navigator.nodes[2]),
        ]
        for char_pos, expected_result in cases:
            self.assertEqual(
                self.navigator.get_closest_node(char_pos),
                expected_result,
            )
