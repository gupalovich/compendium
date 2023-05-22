from unittest import TestCase

import numpy as np

from infra.common.entities import Location, Rect

from ..window import Window, WindowFocusException, WindowNotFoundException


class TestWindow(TestCase):
    def setUp(self) -> None:
        self.window = Window()
        self.process_name = "Calculator"

    def test_find_window(self):
        result = self.window.find_window(self.process_name)
        self.assertIsInstance(result, int)

    def test_find_window_exception_raised_when_window_not_found(self):
        with self.assertRaises(WindowNotFoundException):
            self.window.find_window("nonexistent_process_name")

    def test_get_window_rect(self):
        rect = self.window.get_window_rect(self.process_name)
        # Verify if the top left and bottom right coordinates are within the expected range
        self.assertIsInstance(rect, Rect)
        self.assertGreaterEqual(rect.top_left.x, 0)
        self.assertGreaterEqual(rect.top_left.y, 0)
        self.assertGreater(rect.bottom_right.x, rect.top_left.x)
        self.assertGreater(rect.bottom_right.y, rect.top_left.y)

    def test_grab_mss(self):
        result = self.window.grab_mss()
        self.assertIsInstance(result, np.ndarray)
        self.assertGreater(result.shape[0], 0)
        self.assertGreater(result.shape[1], 0)
        self.assertEqual(result.shape[2], 3)

    def test_grab_mss_with_region(self):
        result = self.window.grab_mss(left=100, top=100, width=100, height=100)
        self.assertIsInstance(result, np.ndarray)
        self.assertGreater(result.shape[0], 0)
        self.assertGreater(result.shape[1], 0)
        self.assertEqual(result.shape[2], 3)

    def test_grab(self):
        result = self.window.grab(
            region=Rect(top_left=Location(100, 100), bottom_right=Location(200, 200))
        )
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape[0], 100)
        self.assertEqual(result.shape[1], 100)
        self.assertEqual(result.shape[2], 3)

    def test_grab_without_region(self):
        result = self.window.grab()
        self.assertIsInstance(result, np.ndarray)
        self.assertGreater(result.shape[0], 0)
        self.assertGreater(result.shape[1], 0)
        self.assertEqual(result.shape[2], 3)

    def test_focus(self):
        hwin = self.window.find_window(self.process_name)
        self.window.focus(hwin)

    def test_focus_unknown(self):
        with self.assertRaises(WindowFocusException):
            self.window.focus(999)
