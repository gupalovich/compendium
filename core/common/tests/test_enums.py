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
        self.state_len = 9

    def test_attribute_length(self):
        self.assertEqual(len(State), self.state_len)

    def test_attribute_names(self):
        self.assertEqual(State.INIT.name, "INIT")
        self.assertEqual(State.SEARCHING.name, "SEARCHING")
        self.assertEqual(State.NAVIGATING.name, "NAVIGATING")
        self.assertEqual(State.MOUNTING.name, "MOUNTING")
        self.assertEqual(State.GATHERING.name, "GATHERING")
        self.assertEqual(State.KILLING.name, "KILLING")

        self.assertEqual(State.IDLE.name, "IDLE")
        self.assertEqual(State.START.name, "START")
        self.assertEqual(State.DONE.name, "DONE")

    def test_attribute_values(self):
        self.assertEqual(State.INIT.value, 1)
