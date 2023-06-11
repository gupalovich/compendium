# import os
# from unittest import TestCase, skip

# from config import settings
# from core.common.entities import Img, Pixel, Polygon, Rect
# from core.common.enums import ColorFormat
# from core.display.window import WindowHandler

# from ..utils import (
#     convert_img_color,
#     crop_img,
#     crop_polygon_img,
#     draw_circles,
#     draw_crosshairs,
#     draw_lines,
#     draw_rectangles,
#     load_img,
#     resize_img,
#     save_img,
#     show_img,
# )


# class UtilsTests(TestCase):
#     def setUp(self) -> None:
#         self.window = WindowHandler()
#         self.static_path = settings.STATIC_PATH
#         self.img_path = "tests/vision/test_template.png"
#         self.img_w = 219
#         self.img_h = 319
#         self.img_channels = 3

#     def test_draw_rectangles(self):
#         img = self.window.grab_mss()
#         left_top = Pixel(50, 50)
#         right_bottom = Pixel(150, 150)
#         rectangles = [Rect(left_top=left_top, right_bottom=right_bottom)]
#         draw_rectangles(img, rectangles)
#         # Show img
#         # show_img(img)

#     def test_draw_crosshairs(self):
#         img = self.window.grab_mss()
#         left_top = Pixel(50, 50)
#         right_bottom = Pixel(150, 150)
#         rectangles = [Rect(left_top=left_top, right_bottom=right_bottom)]
#         draw_crosshairs(img, rectangles)
#         # Show img
#         # show_img(img)

#     def test_draw_circles(self):
#         img = self.window.grab_mss()
#         left_top = Pixel(50, 50)
#         right_bottom = Pixel(150, 150)
#         rectangles = [Rect(left_top=left_top, right_bottom=right_bottom)]
#         draw_circles(img, rectangles, radius=20)
#         # Show img
#         # show_img(img)

#     def test_draw_lines(self):
#         img = self.window.grab_mss()
#         left_top = Pixel(50, 50)
#         right_bottom = Pixel(150, 150)
#         rectangles = [Rect(left_top=left_top, right_bottom=right_bottom)]
#         draw_lines(img, rectangles)
#         # Show img
#         # show_img(img)
