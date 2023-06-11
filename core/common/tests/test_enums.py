from unittest import TestCase

import cv2 as cv

from ..enums import ColorFormat, State


class ColorFormatTests(TestCase):
    def test_attributes(self):
        self.assertEqual(ColorFormat.BGR, cv.IMREAD_COLOR)
        self.assertEqual(ColorFormat.GRAY, cv.IMREAD_GRAYSCALE)
        self.assertEqual(ColorFormat.UNCHANGED, cv.IMREAD_UNCHANGED)
        self.assertEqual(ColorFormat.BGR_RGB, cv.COLOR_BGR2RGB)
        self.assertEqual(ColorFormat.BGR_GRAY, cv.COLOR_BGR2GRAY)
        self.assertEqual(ColorFormat.BGR_HSV, cv.COLOR_BGR2HSV)


class StateTests(TestCase):
    def setUp(self) -> None:
        self.state_len = 6

    def test_attribute_length(self):
        self.assertEqual(len(State), self.state_len)

    def test_attribute_names(self):
        self.assertEqual(State.INITIAL.name, "INITIAL")
        self.assertEqual(State.STARTED.name, "STARTED")
        self.assertEqual(State.STOPPED.name, "STOPPED")
        self.assertEqual(State.MOVING.name, "MOVING")
        self.assertEqual(State.GATHERING.name, "GATHERING")
        self.assertEqual(State.SEARCHING.name, "SEARCHING")

    def test_attribute_values(self):
        self.assertEqual(State.INITIAL.value, 0)
        self.assertIsInstance(State.STARTED.value, int)
        self.assertIsInstance(State.STOPPED.value, int)
        self.assertIsInstance(State.MOVING.value, int)
        self.assertIsInstance(State.GATHERING.value, int)
        self.assertIsInstance(State.SEARCHING.value, int)
