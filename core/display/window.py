from time import time

import cv2 as cv
import mss
import numpy as np
import win32con
import win32gui
import win32ui

from config import settings
from core.common.entities import Img, Pixel, Rect

from .utils import draw_rectangles


class WindowException(Exception):
    """Base class for exceptions in this module."""


class WindowNotFoundException(WindowException):
    """Exception raised when window is not found."""


class WindowFocusException(WindowException):
    """Exception raised when focus on window is not successful."""


class WindowHandler:
    """Class to handle window actions. It can handle both screen and specific window mode."""

    def __init__(self, process_name: str = None) -> None:
        self.name = process_name
        self.handle = None
        self.dimensions = None
        self._set_handle()
        self._set_dimensions()

    def _set_handle(self):
        """Set class handle by process name or desktop"""
        if self.name:
            self.handle = self.find_window(self.name)
        else:
            self.handle = self.get_desktop_handle()

    def _set_dimensions(self):
        """Set class dimensions by process name or desktop"""
        if self.name:
            self.dimensions = self.get_window_rect(self.name)
        else:
            self.dimensions = self.get_desktop_rect()

    @classmethod
    def get_desktop_handle(cls) -> int:
        return win32gui.GetDesktopWindow()

    @classmethod
    def get_desktop_rect(cls) -> Rect:
        handle = cls.get_desktop_handle()
        left, top, right, bottom = win32gui.GetWindowRect(handle)
        return Rect(left_top=Pixel(left, top), right_bottom=Pixel(right, bottom))

    @classmethod
    def find_window(cls, process_name: str) -> int:
        """Find window by exact process name"""
        hwin = win32gui.FindWindow(None, str(process_name))
        if not hwin:
            raise WindowNotFoundException(f"Process name not found - {process_name}")
        return hwin

    @classmethod
    def get_window_rect(cls, process_name: str) -> Rect:
        """Find window rectangle by process name."""
        hwin = cls.find_window(process_name)
        left, top, right, bottom = win32gui.GetWindowRect(hwin)
        return Rect(left_top=Pixel(left, top), right_bottom=Pixel(right, bottom))

    def focus(self) -> None:
        """Set window to focused state using self.handle"""
        try:
            win32gui.SetForegroundWindow(self.handle)
        except win32gui.error as e:
            raise WindowFocusException(
                f"Error occurred while setting window focus: {e}"
            ) from e

    def grab_mss(self, region: Rect = None) -> Img:
        region = region or self.dimensions
        stc = mss.mss()
        scr = stc.grab(
            {
                "left": region.left_top.x,
                "top": region.left_top.y,
                "width": region.width,
                "height": region.height,
            }
        )
        img = np.array(scr)
        stc.close()
        return Img(data=img)

    def grab(self, region: Rect = None) -> Img:
        """
        Grab the window with optimized parameters for maximum speed boost.
        This function has 1.5-2x speed boost compared to grab_mss() function.

        #### Grab all monitors:
        :width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        :height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        :left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        :top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        """
        region = region or self.dimensions
        left, top = region.left_top
        width = region.width
        height = region.height

        hwindc = win32gui.GetWindowDC(self.handle)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype="uint8")
        img.shape = (height, width, 4)

        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(self.handle, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return Img(data=img)

    def live_screenshot(self, exit_key="q", screen_key="f") -> None:
        """Simplify process of taking screenshots"""

        model_file_path = "ai/albion/models/best_albion1.0.engine"
        classes = [
            "Heretic",
            "Elemental",
            "Sandstone",
            "Rough Stone",
            "Limestone",
            "Birch",
            "Chestnut",
            "Logs",
            "Copper Ore",
            "Tin Ore",
        ]
        from .vision import YoloVision

        yolo = YoloVision(model_file_path, classes)

        while True:
            screenshot = self.grab()
            targets = yolo.find(screenshot, confidence=0.8)

            screenshot = draw_rectangles(screenshot, targets)

            cv.imshow("Windowshot", screenshot.data)

            loop_time = time()

            if cv.waitKey(1) == ord(screen_key):
                print("[INFO] Windowshot taken...")
                screenshot.reset()
                cv.imwrite(f"static/screenshots/{loop_time}.jpg", screenshot.data)
            # if cv.waitKey(1) == ord(exit_key):
            #     cv.destroyAllWindows()
            #     break
        print("[INFO] Done.")


if __name__ == "__main__":
    window = WindowHandler(settings.DEFAULT["process_name"])
    window.live_screenshot()
