import random
from time import sleep

import numpy as np
import win32api

from .core import Keys

keys = Keys()


def set_cursor(x, y):
    win32api.SetCursorPos((x, y))


def reset_cursor(x, y) -> None:
    """
    cursor_reset = reset_cursor(move_x, move_y)
    if cursor_reset:
        break
    """
    if x >= 1900 or x <= 20:
        boundary_x = 1920 if x > 1900 else 0
        win32api.SetCursorPos((boundary_x, y))
        sleep(0.1)
        return True
    return False


def wind_mouse(
    start_x,
    start_y,
    dest_x,
    dest_y,
    G_0=12,
    W_0=3,
    M_0=13,
    D_0=13,
    delay=False,
):
    """
    WindMouse algorithm. Calls the set_cursor with each new step.
    G_0 - magnitude of the gravitational force
    W_0 - magnitude of the wind force fluctuations
    M_0 - maximum step size (velocity clip threshold)
    D_0 - distance where wind behavior changes from random to damped
    """
    sqrt3 = np.sqrt(3)
    sqrt5 = np.sqrt(5)
    current_x, current_y = start_x, start_y
    v_x = v_y = W_x = W_y = 0
    while (dist := np.hypot(dest_x - start_x, dest_y - start_y)) >= 1:
        W_mag = min(W_0, dist)
        if dist >= D_0:
            W_x = W_x / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
            W_y = W_y / sqrt3 + (2 * np.random.random() - 1) * W_mag / sqrt5
        else:
            W_x /= sqrt3
            W_y /= sqrt3
            if M_0 < 3:
                M_0 = np.random.random() * 3 + 3
            else:
                M_0 /= sqrt5
        v_x += W_x + G_0 * (dest_x - start_x) / dist
        v_y += W_y + G_0 * (dest_y - start_y) / dist
        v_mag = np.hypot(v_x, v_y)
        if v_mag > M_0:
            v_clip = M_0 / 2 + np.random.random() * M_0 / 2
            v_x = (v_x / v_mag) * v_clip
            v_y = (v_y / v_mag) * v_clip
        start_x += v_x
        start_y += v_y
        move_x = int(np.round(start_x))
        move_y = int(np.round(start_y))

        if current_x != move_x or current_y != move_y:
            # This should wait for the mouse polling interval
            set_cursor(current_x := move_x, current_y := move_y)
            if delay:
                sleep(0.00001)
    return current_x, current_y


def move_camera(x: int, y: int, step=13, delay=True) -> None:
    """Move from current position_x + x; current position_y + y
    Increase step to accelerate"""
    pos_x, pos_y = win32api.GetCursorPos()
    x += pos_x
    y += pos_y
    wind_mouse(pos_x, pos_y, x, y, M_0=step, D_0=step, delay=delay)


def move_to(x: int, y: int, delay=0.2) -> None:
    pos_x, pos_y = win32api.GetCursorPos()
    wind_mouse(pos_x, pos_y, x, y)
    if delay:
        sleep(delay)


def click(button="left", clicks=1) -> None:
    buttons = {
        "left": {"press": keys.mouse_lb_press, "release": keys.mouse_lb_release},
        "right": {"press": keys.mouse_rb_press, "release": keys.mouse_rb_release},
    }
    for _ in range(clicks):
        keys.directMouse(buttons=buttons[button]["press"])
        sleep(random.uniform(0.1, 0.25))
        keys.directMouse(buttons=buttons[button]["release"])


def press(key: str, delay=0) -> None:
    keys.directKey(key)
    sleep(random.uniform(0.1, 0.25))
    keys.directKey(key, keys.key_release)
    if delay:
        sleep(delay)
