from unittest import TestCase

import cv2 as cv

from config import settings
from core.common.entities import ImgLoader, Pixel, Rect, SearchResult

from ..vision import VisionBase


class VisionBaseTests(TestCase):
    def setUp(self) -> None:
        self.static_path = settings.STATIC_PATH
        self.vision = VisionBase()
        self.search_img = ImgLoader("tests/vision/test_screen.png")
        self.ref_img = ImgLoader("tests/vision/test_template.png", conf=0.5)
        self.ref_img1 = ImgLoader("tests/vision/test_template1.png", conf=0.5)

    def test_attributes(self):
        self.assertEqual(self.vision.method, cv.TM_CCOEFF_NORMED)
        self.assertIsInstance(self.vision.cropped_areas, dict)
        self.assertIsInstance(self.vision.ui_elements, dict)

    def test_match_template(self):
        result = self.vision.match_template(
            self.ref_img, self.search_img, confidence=0.95
        )
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)

    def test_match_template_not_found(self):
        result = self.vision.match_template(
            self.ref_img1, self.search_img, confidence=0.8
        )
        self.assertIsInstance(result, list)
        self.assertFalse(len(result))

    def test_find(self):
        crop = Rect(left_top=Pixel(100, 100), right_bottom=Pixel(600, 600))
        test_cases = [
            (self.ref_img, self.search_img),
            (self.ref_img, self.search_img, crop),
        ]

        for test_case in test_cases:
            result = self.vision.find(*test_case)
            # Test result
            self.assertIsInstance(result, SearchResult)
            self.assertEqual(len(result), 1)
            for loc in result.locations:
                self.assertEqual(loc.left_top.x, 223)
                self.assertEqual(loc.left_top.y, 175)
                self.assertEqual(loc.width, 219)
                self.assertEqual(loc.height, 319)

    def test_find_with_no_result(self):
        result = self.vision.find(
            self.ref_img1,
            self.search_img,
        )
        # Test result
        self.assertIsInstance(result, SearchResult)
        self.assertFalse(len(result))
