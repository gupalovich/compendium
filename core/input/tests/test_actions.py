import pytest
import win32api

from ..actions import click, move_to, press, reset_cursor, set_cursor, wind_mouse


@pytest.mark.slow
def test_set_cursor():
    set_cursor(0, 0)
    pos_x, pos_y = win32api.GetCursorPos()
    assert pos_x == 0
    assert pos_y == 0


@pytest.mark.slow
def test_reset_cursor():
    res = reset_cursor(1900, 100)
    assert res is True
    res = reset_cursor(20, 100)
    assert res is True
    res = reset_cursor(100, 100)
    assert res is False


@pytest.mark.slow
def test_wind_mouse():
    pos_x, pos_y = win32api.GetCursorPos()
    wind_mouse(pos_x, pos_y, 100, 100)


@pytest.mark.slow
def test_move_to():
    pos_x, pos_y = win32api.GetCursorPos()
    move_to(100, 100)
    assert pos_x == 100
    assert pos_y == 100


@pytest.mark.slow
def test_click():
    click(clicks=2)
    click(button="right")
    click(button="left")


@pytest.mark.slow
def test_press():
    press("a")
    press("b")
    press("c")
    press("c", delay=0.3)
