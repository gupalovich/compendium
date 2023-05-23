from dataclasses import asdict
from unittest import TestCase

import numpy as np

from ..entities import Coord, Img, MatchLocation, Rect


class LocationTests(TestCase):
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
    def test_attributes(self):
        top_left = Coord(x=10.5, y=20.5)
        bottom_right = Coord(x=30.5, y=40.5)
        rect = Rect(top_left=top_left, bottom_right=bottom_right)

        self.assertEqual(rect.top_left, top_left)
        self.assertEqual(rect.bottom_right, bottom_right)

    def test_iteration(self):
        top_left = Coord(x=10.5, y=20.5)
        bottom_right = Coord(x=30.5, y=40.5)
        rect = Rect(top_left=top_left, bottom_right=bottom_right)

        rect_values = list(rect)
        expected_values = [top_left.x, top_left.y, bottom_right.x, bottom_right.y]
        self.assertEqual(rect_values, expected_values)

    def test_width(self):
        top_left = Coord(x=10.5, y=20.5)
        bottom_right = Coord(x=30.5, y=40.5)
        rect = Rect(top_left=top_left, bottom_right=bottom_right)

        self.assertEqual(rect.width, bottom_right.x - top_left.x)

    def test_height(self):
        top_left = Coord(x=10.5, y=20.5)
        bottom_right = Coord(x=30.5, y=40.5)
        rect = Rect(top_left=top_left, bottom_right=bottom_right)

        self.assertEqual(rect.height, bottom_right.y - top_left.y)

    def test_center(self):
        top_left = Coord(x=10.5, y=20.5)
        bottom_right = Coord(x=30.5, y=40.5)
        rect = Rect(top_left=top_left, bottom_right=bottom_right)

        center = rect.center()
        expected_center = Coord(
            x=(top_left.x + bottom_right.x) / 2, y=(top_left.y + bottom_right.y) / 2
        )
        self.assertEqual(center, expected_center)

    def test_immutable(self):
        rect = Rect(top_left=Coord(x=10.5, y=20.5), bottom_right=Coord(x=30.5, y=40.5))

        with self.assertRaises(AttributeError):
            rect.top_left = Coord(x=50.5, y=60.5)

    def test_rect_asdict(self):
        top_left = Coord(x=10.5, y=20.5)
        bottom_right = Coord(x=30.5, y=40.5)
        rect = Rect(top_left=top_left, bottom_right=bottom_right)

        rect_dict = asdict(rect)
        expected_dict = {
            "top_left": {"x": top_left.x, "y": top_left.y},
            "bottom_right": {"x": bottom_right.x, "y": bottom_right.y},
        }
        self.assertEqual(rect_dict, expected_dict)


class ProcessedImgTests(TestCase):
    def setUp(self) -> None:
        self.width = 10
        self.height = 15

    def test_attributes(self):
        img = np.zeros((self.width, self.height), dtype=np.uint8)
        processed_img = Img(img=img, width=self.width, height=self.height)

        self.assertTrue(np.array_equal(processed_img.img, img))
        self.assertEqual(processed_img.width, self.width)
        self.assertEqual(processed_img.height, self.height)

    def test_iteration(self):
        img = np.zeros((self.width, self.height), dtype=np.uint8)
        processed_img = Img(img=img, width=self.width, height=self.height)

        img_value, width_value, height_value = processed_img
        self.assertTrue(np.array_equal(img_value, img))
        self.assertEqual(width_value, self.width)
        self.assertEqual(height_value, self.height)

    def test_immutable(self):
        img = np.zeros((self.width, self.height), dtype=np.uint8)
        processed_img = Img(img=img, width=self.width, height=self.height)

        with self.assertRaises(AttributeError):
            processed_img.img = np.ones((10, 10), dtype=np.uint8)

    def test_equality(self):
        img1 = np.zeros((self.width, self.height), dtype=np.uint8)
        img2 = np.zeros((self.width, self.height), dtype=np.uint8)
        processed_img1 = Img(img=img1, width=self.width, height=self.height)
        processed_img2 = Img(img=img2, width=self.width, height=self.height)

        self.assertEqual(processed_img1, processed_img2)

    def test_inequality(self):
        img1 = np.zeros((self.width, self.height), dtype=np.uint8)
        img2 = np.zeros((100, 100), dtype=np.uint8)
        processed_img1 = Img(img=img1, width=self.width, height=self.height)
        processed_img2 = Img(img=img2, width=100, height=100)

        self.assertNotEqual(processed_img1, processed_img2)


class MatchLocationTests(TestCase):
    def test_attributes(self):
        top_left = Coord(x=10.5, y=20.5)
        width = 100
        height = 200
        confidence = 0.75

        match_info = MatchLocation(
            top_left=top_left,
            width=width,
            height=height,
            confidence=confidence,
        )

        self.assertEqual(match_info.top_left, top_left)
        self.assertEqual(match_info.width, width)
        self.assertEqual(match_info.height, height)
        self.assertEqual(match_info.confidence, confidence)

    def test_as_rect(self):
        top_left = Coord(x=10.5, y=20.5)
        width = 100
        height = 200
        confidence = 0.75

        match_info = MatchLocation(
            top_left=top_left,
            width=width,
            height=height,
            confidence=confidence,
        )

        expected_rect = Rect(
            top_left=top_left,
            bottom_right=Coord(
                x=top_left.x + width,
                y=top_left.y + height,
            ),
        )

        rect = match_info.as_rect()

        self.assertEqual(rect, expected_rect)
