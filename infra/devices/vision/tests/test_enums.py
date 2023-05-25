from unittest import TestCase

import cv2 as cv

from ..enums import ColorFormat


class ColorFormatTests(TestCase):
    def test_attributes(self):
        self.assertEqual(ColorFormat.BGR, cv.IMREAD_COLOR)
        self.assertEqual(ColorFormat.GRAY, cv.IMREAD_GRAYSCALE)
        self.assertEqual(ColorFormat.UNCHANGED, cv.IMREAD_UNCHANGED)
        self.assertEqual(ColorFormat.BGR_RGB, cv.COLOR_BGR2RGB)
        self.assertEqual(ColorFormat.BGR_GRAY, cv.COLOR_BGR2GRAY)
        self.assertEqual(ColorFormat.BGR_HSV, cv.COLOR_BGR2HSV)
