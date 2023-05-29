from dataclasses import asdict
from unittest import TestCase

import cv2 as cv
import numpy as np

from ..entities import Color, Coord, DetectedObjects, Img, Polygon, Rect


class CoordTests(TestCase):
    def test_attributes(self):
        x = 10.5
        y = 20.5
        loc = Coord(x=x, y=y)

        self.assertEqual(loc.x, x)
        self.assertEqual(loc.y, y)

    def test_iteration(self):
        x = 10.5
        y = 20.5
        loc = Coord(x=x, y=y)

        coordinates = list(loc)
        self.assertEqual(coordinates, [x, y])

    def test_immutable(self):
        loc = Coord(x=10.5, y=20.5)

        with self.assertRaises(AttributeError):
            loc.x = 30.5

    def test_equality(self):
        loc1 = Coord(x=10.5, y=20.5)
        loc2 = Coord(x=10.5, y=20.5)
        loc3 = Coord(x=30.5, y=40.5)

        self.assertEqual(loc1, loc2)
        self.assertNotEqual(loc1, loc3)

    def test_asdict(self):
        x = 10.5
        y = 20.5
        loc = Coord(x=x, y=y)

        loc_dict = asdict(loc)
        self.assertEqual(loc_dict, {"x": x, "y": y})


class RectTests(TestCase):
    def setUp(self) -> None:
        self.left_top = Coord(x=10.5, y=20.5)
        self.right_bottom = Coord(x=30.5, y=40.5)
        self.width = 20
        self.height = 20

    def test_post_init_attributes_validation(self):
        err_msg = "Either right_bottom or both width and height must be provided."

        test_cases = [
            {"left_top": self.left_top},
            {"left_top": self.left_top, "width": self.width},
            {"left_top": self.left_top, "height": self.height},
        ]

        for kwargs in test_cases:
            with self.assertRaisesRegex(ValueError, err_msg):
                Rect(**kwargs)

    def test_attributes(self):
        width = self.right_bottom.x - self.left_top.x
        height = self.right_bottom.y - self.left_top.y
        expected_center_x = round((self.left_top.x + self.right_bottom.x) / 2)
        expected_center_y = round((self.left_top.y + self.right_bottom.y) / 2)

        test_cases = [
            {"left_top": self.left_top, "right_bottom": self.right_bottom},
            {"left_top": self.left_top, "width": self.width, "height": self.height},
        ]

        for kwargs in test_cases:
            rect = Rect(**kwargs)
            self.assertEqual(rect.left_top, self.left_top)
            self.assertEqual(rect.right_bottom, self.right_bottom)
            self.assertEqual(rect.width, width)
            self.assertEqual(rect.height, height)
            self.assertEqual(rect.center.x, expected_center_x)
            self.assertEqual(rect.center.y, expected_center_y)

    def test_iteration(self):
        rect = Rect(left_top=self.left_top, right_bottom=self.right_bottom)
        rect_values = list(rect)
        expected_values = [self.left_top, self.right_bottom, self.width, self.height]
        self.assertEqual(rect_values, expected_values)

    def test_rect_asdict(self):
        rect = Rect(left_top=self.left_top, right_bottom=self.right_bottom)
        rect_dict = asdict(rect)
        expected_dict = {
            "left_top": {"x": self.left_top.x, "y": self.left_top.y},
            "right_bottom": {"x": self.right_bottom.x, "y": self.right_bottom.y},
            "width": self.width,
            "height": self.height,
        }
        self.assertEqual(rect_dict, expected_dict)


class PolygonTests(TestCase):
    def test_valid_polygon(self):
        points = [
            Coord(x=0, y=0),
            Coord(x=0, y=1),
            Coord(x=1, y=1),
            Coord(x=1, y=0),
        ]
        polygon = Polygon(points)
        self.assertEqual(polygon.points, points)

    def test_invalid_polygon(self):
        points = [
            Coord(x=0, y=0),
            Coord(x=0, y=1),
            Coord(x=1, y=1),
        ]
        with self.assertRaises(ValueError):
            Polygon(points)

    def test_as_np_array(self):
        points = [
            Coord(x=0, y=0),
            Coord(x=0, y=1),
            Coord(x=1, y=1),
            Coord(x=1, y=0),
        ]
        polygon = Polygon(points)
        expected_np_array = np.array([(0, 0), (0, 1), (1, 1), (1, 0)])
        np.testing.assert_array_equal(polygon.as_np_array(), expected_np_array)


class ImgTests(TestCase):
    def setUp(self) -> None:
        self.img = cv.imread("static/tests/vision/test_template.png")
        self.height = self.img.shape[0]
        self.width = self.img.shape[1]
        self.channels = self.img.shape[2]

    def test_attributes(self):
        test_cases = [
            {"data": self.img},
            {"data": self.img, "width": self.width, "height": self.height},
            {"data": self.img, "width": 123, "height": 123},
        ]
        for kwargs in test_cases:
            img = Img(**kwargs)
            self.assertEqual(img.width, self.width)
            self.assertEqual(img.height, self.height)
            self.assertEqual(img.channels, self.channels)

    def test_iteration(self):
        img = Img(self.img)
        img_values = list(img)
        expected_values = [self.img, self.width, self.height, self.channels]
        self.assertEqual(img_values, expected_values)


class ColorTests(TestCase):
    def test_color_creation_valid_rgb(self):
        # Test creating Color object with valid RGB values
        color = Color(r=255, g=128, b=64)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 128)
        self.assertEqual(color.b, 64)
        self.assertIsNone(color.a)

    def test_color_creation_valid_rgba(self):
        # Test creating Color object with valid RGBA values
        color = Color(r=255, g=128, b=64, a=200)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 128)
        self.assertEqual(color.b, 64)
        self.assertEqual(color.a, 200)

    def test_color_creation_invalid_rgb(self):
        # Test creating Color object with invalid RGB values
        with self.assertRaises(ValueError):
            Color(r=-1, g=128, b=64)

        with self.assertRaises(ValueError):
            Color(r=255, g=300, b=64)

        with self.assertRaises(ValueError):
            Color(r=255, g=128, b=-10)

    def test_color_creation_invalid_rgba(self):
        # Test creating Color object with invalid RGBA values
        with self.assertRaises(ValueError):
            Color(r=255, g=128, b=64, a=-1)

        with self.assertRaises(ValueError):
            Color(r=255, g=128, b=64, a=300)

    def test_from_rgb(self):
        # Test creating Color object from RGB values
        rgb = (100, 150, 200)
        color = Color.from_rgb(rgb)
        self.assertEqual(color.r, 100)
        self.assertEqual(color.g, 150)
        self.assertEqual(color.b, 200)
        self.assertIsNone(color.a)

    def test_from_rgb_invalid(self):
        err_msg = "Invalid RGB values. Expected a tuple of length 3 or 4."
        with self.assertRaisesRegex(ValueError, err_msg):
            Color.from_rgb((200, 150, 100, 0, 0))

    def test_from_bgr(self):
        # Test creating Color object from BGR values
        bgr = (200, 150, 100)
        color = Color.from_bgr(bgr)
        self.assertEqual(color.r, 100)
        self.assertEqual(color.g, 150)
        self.assertEqual(color.b, 200)
        self.assertIsNone(color.a)

    def test_from_bgr_invalid(self):
        err_msg = "Invalid BGR values. Expected a tuple of length 3 or 4."
        with self.assertRaisesRegex(ValueError, err_msg):
            Color.from_bgr((200, 150, 100, 0, 0))

    def test_to_rgb(self):
        # Test converting Color object to RGB values
        color = Color(r=100, g=150, b=200, a=50)
        rgb = color.to_rgb()
        self.assertEqual(rgb, (100, 150, 200, 50))

        color = Color(r=100, g=150, b=200)
        rgb = color.to_rgb()
        self.assertEqual(rgb, (100, 150, 200))

    def test_to_bgr(self):
        # Test converting Color object to BGR values
        color = Color(r=100, g=150, b=200, a=50)
        bgr = color.to_bgr()
        self.assertEqual(bgr, (200, 150, 100, 50))

        color = Color(r=100, g=150, b=200)
        bgr = color.to_bgr()
        self.assertEqual(bgr, (200, 150, 100))

    def test_asdict(self):
        # Test converting Color object to dictionary
        color = Color(r=100, g=150, b=200, a=50)
        color_dict = asdict(color)
        expected_dict = {
            "r": 100,
            "g": 150,
            "b": 200,
            "a": 50,
        }
        self.assertEqual(color_dict, expected_dict)

        color = Color(r=100, g=150, b=200)
        color_dict = asdict(color)
        expected_dict = {
            "r": 100,
            "g": 150,
            "b": 200,
            "a": None,
        }
        self.assertEqual(color_dict, expected_dict)


class DetectedObjectsTests(TestCase):
    def setUp(self):
        self.ref_img = Img(data=np.zeros((10, 10), dtype=np.uint8))
        self.search_img = Img(data=np.zeros((20, 20), dtype=np.uint8))
        self.confidence = 0.8
        self.rect1 = Rect(left_top=Coord(x=5, y=5), right_bottom=Coord(x=15, y=15))
        self.rect2 = Rect(left_top=Coord(x=10, y=10), right_bottom=Coord(x=20, y=20))
        self.detected_objects = DetectedObjects(
            ref_img=self.ref_img, search_img=self.search_img, confidence=self.confidence
        )

    def test_attributes(self):
        self.assertEqual(self.detected_objects.ref_img, self.ref_img)
        self.assertEqual(self.detected_objects.search_img, self.search_img)
        self.assertEqual(self.detected_objects.confidence, self.confidence)
        self.assertEqual(self.detected_objects.locations, [])

    def test_size(self):
        self.detected_objects.locations = [self.rect1, self.rect2]
        self.assertEqual(self.detected_objects.size(), 2)

    def test_add(self):
        self.detected_objects.add(self.rect1)
        self.assertEqual(self.detected_objects.size(), 1)
        self.assertEqual(self.detected_objects.locations, [self.rect1])

        self.detected_objects.add(self.rect2)
        self.assertEqual(self.detected_objects.size(), 2)
        self.assertEqual(self.detected_objects.locations, [self.rect1, self.rect2])

    def test_remove(self):
        with self.assertRaises(NotImplementedError):
            self.detected_objects.remove()
