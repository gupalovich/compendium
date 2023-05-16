import numpy as np
import win32api
import win32con
import win32gui
import win32ui

from infrastructure.common.entities import Rect2D
from infrastructure.vision.opencv import open_cv


class ScreenException(Exception):
    """Base class for exceptions in this module."""


class ScreenNotFoundException(ScreenException):
    """Exception raised when screen is not found."""


class Screen:
    """Class to represent a screen"""

    process_name = None

    @classmethod
    def grab(cls, rect: Rect2D = None) -> np.ndarray:
        """Grab the screen with optimized parameters for maximum speed boost

        TODO: fix win32gui.FindWindow with process_name - searches exact process name
        TODO: Refactor primitives
        """

        if cls.process_name:
            hwin = win32gui.FindWindow(None, cls.process_name)
            if not hwin:
                raise ScreenNotFoundException(
                    f"Process name not found - {cls.process_name}"
                )
        else:
            hwin = win32gui.GetDesktopWindow()

        if cls.process_name:
            left, top, bottom, right = win32gui.GetWindowRect(hwin)
            width = bottom - left
            height = right - left
        elif rect:
            left, top, bottom, right = rect
            width = bottom - left + 1
            height = right - top + 1
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

        return open_cv.cvt_img_rgb(img)

    def crop(self, rect: Rect2D) -> None:
        pass

    def focus(self) -> None:
        pass
