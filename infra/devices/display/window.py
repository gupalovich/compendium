from time import time

import cv2 as cv
import mss
import numpy as np
import win32api
import win32con
import win32gui
import win32ui

from config import settings
from infra.common.entities import Coord, Img, Rect


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
        return Rect(top_left=Coord(top, left), bottom_right=Coord(bottom, right))

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
        rect = Rect(top_left=Coord(top, left), bottom_right=Coord(bottom, right))
        return rect

    def grab_mss(
        self, region: Rect = Rect(top_left=Coord(0, 0), width=1920, height=1080)
    ) -> Img:
        """Grab window by using mss library"""
        stc = mss.mss()
        scr = stc.grab(
            {
                "left": region.top_left.x,
                "top": region.top_left.y,
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
        By default, grabs all screens combined.
        """

        if not self.name:
            self.handle = win32gui.GetDesktopWindow()

        if self.name:
            left, top, bottom, right = win32gui.GetWindowRect(self.handle)
            width = bottom - left
            height = right - left
        elif region:
            left, top, bottom, right = region
            width = region.width
            height = region.height
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

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

    def focus(self, handle: int = None) -> None:
        """Set window to focused state

        Attributes:
            handle: Optional(int), otherwise self.handle
        """
        try:
            handle = handle if handle else self.handle
            win32gui.SetForegroundWindow(handle)
        except win32gui.error as e:
            raise WindowFocusException(
                f"Error occurred while setting window focus: {e}"
            ) from e

    def live_screenshot(self, process_name: str, exit_key="q", screen_key="f") -> None:
        """Simplify process of taking screenshots"""

        window_rect = self.get_window_rect(process_name)

        while True:
            screenshot = self.grab(window_rect)

            cv.imshow("Windowshot", screenshot)

            loop_time = time()

            key = cv.waitKey(1)

            if key == ord(exit_key):
                cv.destroyAllWindows()
                break
            if key == ord(screen_key):
                print("[INFO] Windowshot taken...")
                cv.imwrite(f"static/screenshots/{loop_time}.jpg", screenshot)
        print("[INFO] Done.")


if __name__ == "__main__":
    window = WindowHandler()
    window.live_screenshot(settings.DEFAULT["process_name"])
