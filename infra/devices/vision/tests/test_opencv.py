from unittest import TestCase

from config import settings
from infra.common.entities import Coord, DetectedObjects, Rect

from ..opencv import OpenCV
from ..utils import load_img


class OpenCVTests(TestCase):
    def setUp(self) -> None:
        self.static_path = settings.STATIC_PATH
        self.opencv = OpenCV()
        self.search_img = load_img("tests/vision/test_screen.png")
        self.search_img_w = 961
        self.search_img_h = 789
        self.ref_img = load_img("tests/vision/test_template.png")
        self.ref_img1 = load_img("tests/vision/test_template1.png")

    def test__match_template(self):
        result = self.opencv._match_template(
            self.ref_img, self.search_img, confidence=0.95
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test__match_template_not_found(self):
        result = self.opencv._match_template(
            self.ref_img1, self.search_img, confidence=0.8
        )
        self.assertIsInstance(result, list)
        self.assertFalse(len(result))

    def test_find(self):
        conf = 0.5
        result = self.opencv.find(
            self.ref_img,
            self.search_img,
            confidence=conf,
        )
        # Test result
        self.assertIsInstance(result, DetectedObjects)
        self.assertEqual(result.confidence, conf)
        self.assertEqual(len(result), 1)
        for loc in result.locations:
            self.assertEqual(loc.left_top.x, 223)
            self.assertEqual(loc.left_top.y, 175)
            self.assertEqual(loc.width, 219)
            self.assertEqual(loc.height, 319)

    def test_find_with_no_result(self):
        conf = 0.5
        result = self.opencv.find(
            self.ref_img1,
            self.search_img,
            confidence=conf,
        )
        # Test result
        self.assertIsInstance(result, DetectedObjects)
        self.assertEqual(result.confidence, conf)
        self.assertFalse(len(result))

    def test_find_with_crop(self):
        crop = Rect(left_top=Coord(x=100, y=100), right_bottom=Coord(x=700, y=700))
        conf = 0.5
        result = self.opencv.find(
            self.ref_img,
            self.search_img,
            confidence=conf,
            crop=crop,
        )
        # Test result
        self.assertIsInstance(result, DetectedObjects)
        self.assertEqual(result.confidence, conf)
        self.assertEqual(len(result), 1)
        for loc in result.locations:
            self.assertEqual(loc.left_top.x, 223)
            self.assertEqual(loc.left_top.y, 175)
            self.assertEqual(loc.width, 219)
            self.assertEqual(loc.height, 319)
