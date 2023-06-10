from unittest import TestCase

import numpy as np

from core.common.entities import Coord, Img, Rect

from ..window import WindowFocusException, WindowHandler, WindowNotFoundException


class TestWindowHandler(TestCase):
    def setUp(self) -> None:
        self.process_name = "Calculator"

    def test__set_handle_with_name(self):
        window = WindowHandler(self.process_name)
        self.assertEqual(window.name, self.process_name)
        self.assertIsInstance(window.handle, int)

    def test__set_handle_without_name(self):
        window = WindowHandler()
        self.assertEqual(window.name, None)
        self.assertIsInstance(window.handle, int)

    def test__set_dimensions_with_name(self):
        window = WindowHandler(self.process_name)
        self.assertIsInstance(window.dimensions, Rect)
        self.assertLess(window.dimensions.width, 700)
        self.assertLess(window.dimensions.height, 700)

    def test__set_dimensions_without_name(self):
        window = WindowHandler()
        self.assertIsInstance(window.dimensions, Rect)
        self.assertGreaterEqual(window.dimensions.width, 1920)
        self.assertGreaterEqual(window.dimensions.height, 1080)

    def test_get_desktop_handle(self):
        handle = WindowHandler.get_desktop_handle()
        self.assertIsInstance(handle, int)

    def test_get_desktop_rect(self):
        rect = WindowHandler.get_desktop_rect()
        self.assertIsInstance(rect, Rect)
        self.assertGreaterEqual(rect.width, 1920)
        self.assertGreaterEqual(rect.height, 1080)

    def test_find_window(self):
        handle = WindowHandler.find_window(self.process_name)
        self.assertIsInstance(handle, int)

    def test_find_window_exception_raised_when_window_not_found(self):
        with self.assertRaises(WindowNotFoundException):
            WindowHandler.find_window("nonexistent_process_name")

    def test_get_window_rect(self):
        rect = WindowHandler.get_window_rect(self.process_name)
        self.assertIsInstance(rect, Rect)
        self.assertGreaterEqual(rect.left_top.x, 0)
        self.assertGreaterEqual(rect.left_top.y, 0)
        self.assertGreater(rect.right_bottom.x, rect.left_top.x)
        self.assertGreater(rect.right_bottom.y, rect.left_top.y)

    def test_focus_with_name(self):
        window = WindowHandler(self.process_name)
        window.focus()

    def test_focus_unknown(self):
        with self.assertRaises(WindowFocusException):
            window = WindowHandler(self.process_name)
            window.handle = 999
            window.focus()

    def test_grab_mss(self):
        window = WindowHandler()
        result = window.grab_mss()
        self.assertIsInstance(result, Img)
        self.assertIsInstance(result.data, np.ndarray)
        self.assertGreaterEqual(result.data.shape[0], 1080)
        self.assertGreaterEqual(result.data.shape[1], 1920)
        self.assertEqual(result.data.shape[2], 4)

    def test_grab(self):
        window = WindowHandler()
        rect = Rect(left_top=Coord(100, 100), right_bottom=Coord(200, 200))
        result = window.grab(region=rect)
        self.assertIsInstance(result, Img)
        self.assertIsInstance(result.data, np.ndarray)
        self.assertEqual(result.data.shape[0], 100)
        self.assertEqual(result.data.shape[1], 100)
        self.assertEqual(result.data.shape[2], 4)

    def test_grab_without_region(self):
        window = WindowHandler()
        result = window.grab()
        self.assertIsInstance(result, Img)
        self.assertIsInstance(result.data, np.ndarray)
        self.assertGreaterEqual(result.data.shape[0], 1080)
        self.assertGreaterEqual(result.data.shape[1], 1920)
        self.assertEqual(result.data.shape[2], 4)
