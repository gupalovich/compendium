# import os
# from unittest import TestCase

# import cv2 as cv
# import numpy as np

# from config import settings
# from infra.common.entities import Img, MatchLocation

# from ..opencv import OpenCV


# class OpenCVTests(TestCase):
#     def setUp(self) -> None:
#         self.static_path = settings.STATIC_PATH
#         self.screen_path = "tests/test_screen.png"
#         self.screen_img_w = 961
#         self.screen_img_h = 789
#         self.tmplt_path = "tests/test_template.png"
#         self.tmplt_path1 = "tests/test_template1.png"
#         self.opencv = OpenCV()

#     def test_load_img(self):
#         processed_img = self.opencv.load_img(self.screen_path, self.static_path)
#         # Assert the returned value is an instance of Img
#         self.assertIsInstance(processed_img, Img)
#         # Assert the processed image has the correct dimensions
#         self.assertEqual(processed_img.width, self.screen_img_w)
#         self.assertEqual(processed_img.height, self.screen_img_h)
#         # Assert the processed image contains the expected image data
#         expected_img = cv.imread(self.static_path + self.screen_path, 0)
#         np.testing.assert_array_equal(processed_img.img, expected_img)

#     def test_save_img(self):
#         new_img_path = "tests/test_save.png"
#         processed_img = self.opencv.load_img(self.screen_path, self.static_path)
#         self.opencv.save_img(processed_img.img, new_img_path)
#         # Test image was saved
#         processed_img = self.opencv.load_img(new_img_path)
#         self.assertEqual(processed_img.width, self.screen_img_w)
#         self.assertEqual(processed_img.height, self.screen_img_h)
#         # Delete the test image
#         os.remove(self.static_path + new_img_path)

#     def test__match_template(self):
#         screen = self.opencv.load_img(self.screen_path)
#         tmplt = self.opencv.load_img(self.tmplt_path)
#         result = self.opencv._match_template(screen.img, tmplt.img, confidence=0.95)
#         self.assertIsInstance(result, list)
#         self.assertEqual(len(result), 1)

#     def test__match_template_not_found(self):
#         screen = self.opencv.load_img(self.screen_path)
#         tmplt = self.opencv.load_img(self.tmplt_path1)
#         result = self.opencv._match_template(screen.img, tmplt.img, confidence=0.8)
#         self.assertIsInstance(result, list)
#         self.assertFalse(len(result))

#     def test_match(self):
#         screen = self.opencv.load_img(self.screen_path)
#         result = self.opencv.match(screen.img, self.tmplt_path, confidence=0.5)
#         # Test result
#         self.assertEqual(len(result), 1)
#         for match_info in result:
#             self.assertIsInstance(match_info, MatchLocation)
#             self.assertEqual(match_info.confidence, 0.5)
#             self.assertEqual(match_info.left_top.x, 223)
#             self.assertEqual(match_info.left_top.y, 175)
#             self.assertEqual(match_info.width, 219)
#             self.assertEqual(match_info.height, 319)

#     def test_match_not_found(self):
#         screen = self.opencv.load_img(self.screen_path)
#         result = self.opencv.match(screen.img, self.tmplt_path1, confidence=0.5)
#         # Test result
#         self.assertFalse(len(result))
