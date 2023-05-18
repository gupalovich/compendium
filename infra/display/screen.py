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
from infra.keys.listener import key_listener
from infra.vision.opencv import opencv


class ScreenException(Exception):
    """Base class for exceptions in this module."""


class ScreenNotFoundException(ScreenException):
    """Exception raised when screen is not found."""


class Screen:
    """Class to represent a screen"""

    def __init__(self, process_name: str = None) -> None:
        self.process_name = process_name

    def find_window(self, process_name: str) -> int:
        """Find window by process name."""
        hwin = win32gui.FindWindow(None, str(process_name))
        if not hwin:
            raise ScreenNotFoundException(f"Process name not found - {process_name}")
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

        img = np.array(scr)
        img = cv.cvtColor(img, cv.IMREAD_COLOR)

        return opencv.cvt_img_normal(img)

    @time_perf
    def grab(self, region: Rect = None) -> np.ndarray:
        """
        Grab the screen with optimized parameters for maximum speed boost.
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

        return opencv.cvt_img_normal(img)

    def focus(self, hwin: int) -> None:
        """
        Set window to focus

        Attributes:
            hwin (int): Window handle
        """
        win32gui.SetForegroundWindow(hwin)

    def live(self, process_name: str, exit_key="q", screen_key="f") -> None:
        """Simplify process of taking screenshots"""

        window_rect = self.get_window_rect(process_name)

        while True:
            screenshot = self.grab(window_rect)

            cv.imshow("Screenshot", screenshot)

            loop_time = time()

            key = cv.waitKey(1)

            if key == ord(exit_key):
                cv.destroyAllWindows()
                break
            if key == ord(screen_key):
                print("[INFO] Screenshot taken...")
                cv.imwrite(f"static/screenshots/{loop_time}.jpg", screenshot)
        print("[INFO] Done.")


screen = Screen()


if __name__ == "__main__":
    screen.live(settings.DEFAULT["process_name"])
