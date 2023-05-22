from time import time

import cv2 as cv
import mss
import numpy as np
import win32api
import win32con
import win32gui
import win32ui

from config import settings
from infra.common.decorators import time_perf
from infra.common.entities import Location, Rect


class WindowException(Exception):
    """Base class for exceptions in this module."""


class WindowNotFoundException(WindowException):
    """Exception raised when window is not found."""


class WindowFocusException(WindowException):
    """Exception raised when window is not focused."""


class Window:
    def __init__(self, process_name: str = None) -> None:
        self.process_name = process_name

    def find_window(self, process_name: str) -> int:
        """Find window by process name."""
        hwin = win32gui.FindWindow(None, str(process_name))
        if not hwin:
            raise WindowNotFoundException(f"Process name not found - {process_name}")
        return hwin

    def get_window_rect(self, process_name: str) -> Rect:
        """Find window rectangle by process name."""
        hwin = self.find_window(process_name)
        rect = win32gui.GetWindowRect(hwin)
        rect = Rect(
            top_left=Location(rect[0], rect[1]),
            bottom_right=Location(rect[2], rect[3]),
        )
        return rect

    @time_perf
    def grab_mss(self, left=0, top=0, width=1920, height=1080):
        stc = mss.mss()
        scr = stc.grab({"left": left, "top": top, "width": width, "height": height})
        stc.close()
        img = np.array(scr)
        return cv.cvtColor(img, cv.IMREAD_COLOR)

    def grab(self, region: Rect = None) -> np.ndarray:
        """
        Grab the window with optimized parameters for maximum speed boost.
        This function has 1.5-2x speed boost compared to grab_mss() function.

        TODO: fix win32gui.FindWindow with process_name - searches exact process name
        TODO: Refactor primitives
        """

        if self.process_name:
            hwin = self.find_window(self.process_name)
        else:
            hwin = win32gui.GetDesktopWindow()

        if self.process_name:
            left, top, bottom, right = win32gui.GetWindowRect(hwin)
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

        hwindc = win32gui.GetWindowDC(hwin)
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
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return cv.cvtColor(img, cv.IMREAD_COLOR)

    def focus(self, hwin: int) -> None:
        """
        Set window to focused state

        Attributes:
            hwin (int): Window handle
        """
        try:
            win32gui.SetForegroundWindow(hwin)
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
    window = Window()
    window.live_screenshot(settings.DEFAULT["process_name"])
