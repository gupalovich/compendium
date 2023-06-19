from unittest import TestCase, skip

import win32api

from ..actions import Actions


class TestActions(TestCase):
    def setUp(self) -> None:
        self.actions = Actions()

    @skip("Mouse movement and async conflict with too many calls")
    def test_set_cursor(self):
        self.actions.set_cursor(0, 0)
        pos_x, pos_y = win32api.GetCursorPos()
        assert pos_x == 0
        assert pos_y == 0

    @skip("Mouse movement and async conflict with too many calls")
    def test_reset_cursor(self):
        res = self.actions.reset_cursor(1900, 100)
        assert res is True
        res = self.actions.reset_cursor(20, 100)
        assert res is True
        res = self.actions.reset_cursor(100, 100)
        assert res is False

    @skip("Mouse movement and async conflict with too many calls")
    def test_wind_mouse(self):
        pos_x, pos_y = win32api.GetCursorPos()
        self.actions.wind_mouse(pos_x, pos_y, 100, 100)

    @skip("Mouse movement and async conflict with too many calls")
    def test_move_to(self):
        self.actions.move_to(100, 100)
        pos_x, pos_y = win32api.GetCursorPos()
        assert pos_x == 100
        assert pos_y == 100

    @skip("Mouse movement and async conflict with too many calls")
    def test_click(self):
        self.actions.click(clicks=2)
        self.actions.click(button="right")
        self.actions.click(button="left")

    @skip("Mouse movement and async conflict with too many calls")
    def test_press(self):
        self.actions.press("a")
        self.actions.press("b")
        self.actions.press("c")
        self.actions.press("c", delay=0.3)
