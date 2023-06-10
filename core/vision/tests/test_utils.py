import os
from unittest import TestCase, skip

from config import settings
from core.common.entities import Img, Pixel, Polygon, Rect
from core.display.window import WindowHandler
from core.vision.enums import ColorFormat

from ..utils import (
    convert_img_color,
    crop_img,
    crop_polygon_img,
    draw_circles,
    draw_crosshairs,
    draw_lines,
    draw_rectangles,
    load_img,
    resize_img,
    save_img,
    show_img,
)


class UtilsTests(TestCase):
    def setUp(self) -> None:
        self.window = WindowHandler()
        self.static_path = settings.STATIC_PATH
        self.img_path = "tests/vision/test_template.png"
        self.img_w = 219
        self.img_h = 319
        self.img_channels = 3

    def test_load_img(self):
        img = load_img(self.img_path)
        img_list = list(img)
        expected_data = [img.data, self.img_w, self.img_h, self.img_channels]
        self.assertIsInstance(img, Img)
        self.assertEqual(img_list, expected_data)

    def test_load_img_with_static_path_and_format(self):
        img = load_img(self.img_path, static_path="static/", fmt=ColorFormat.UNCHANGED)
        img_list = list(img)
        expected_data = [img.data, self.img_w, self.img_h, self.img_channels]
        self.assertIsInstance(img, Img)
        self.assertEqual(img_list, expected_data)

    def test_load_img_gray(self):
        img = load_img(self.img_path, fmt=ColorFormat.GRAY)
        img_list = list(img)
        expected_data = [img.data, self.img_w, self.img_h, 1]
        self.assertIsInstance(img, Img)
        self.assertEqual(img_list, expected_data)

    def test_save_img(self):
        new_img_path = "tests/test_save.png"
        img = load_img(self.img_path)
        save_img(img, new_img_path)
        # Test image was saved
        img = load_img(new_img_path)
        self.assertEqual(img.width, self.img_w)
        self.assertEqual(img.height, self.img_h)
        self.assertEqual(img.channels, self.img_channels)
        # Delete the test image
        os.remove(self.static_path + new_img_path)

    @skip("Popup window")
    def test_show_img(self):
        img = load_img(self.img_path)
        show_img(img, window_name="Test window")

    def test_resize_image_up(self):
        img = load_img(self.img_path)
        img = resize_img(img, zoom_factor=2)
        self.assertEqual(img.width, self.img_w * 2)
        self.assertEqual(img.height, self.img_h * 2)

    def test_resize_image_down(self):
        img = load_img(self.img_path)
        img = resize_img(img, zoom_factor=0.5)
        self.assertAlmostEqual(img.width, self.img_w / 2, delta=0.5)
        self.assertAlmostEqual(img.height, self.img_h / 2, delta=0.5)

    def test_crop_img(self):
        img = load_img(self.img_path)
        width, height = (150, 100)
        test_cases = [
            {"rect": Rect(left_top=Pixel(0, 0), width=width, height=height)},
            {
                "rect": Rect(
                    left_top=Pixel(50, 75), right_bottom=Pixel(width + 50, height + 75)
                )
            },
        ]
        for case in test_cases:
            new_img = crop_img(img, case["rect"])
            self.assertEqual(new_img.width, width)
            self.assertEqual(new_img.height, height)

    def test_crop_polygon_img(self):
        img = self.window.grab_mss()
        poly = Polygon(
            [Pixel(100, 500), Pixel(500, 250), Pixel(1000, 600), Pixel(500, 800)]
        )
        width, height = 900, 550
        new_img = crop_polygon_img(img, poly)
        # Test image was cropped
        self.assertEqual(new_img.width, width)
        self.assertEqual(new_img.height, height)
        # Test pixel color at (10, 10)
        pixel_color = new_img.data[10, 10]
        expected_color = (0, 0, 0)
        for channel_value, expected_value in zip(pixel_color, expected_color):
            self.assertEqual(channel_value, expected_value)

    def test_convert_img_color(self):
        img = self.window.grab_mss()
        self.assertEqual(img.channels, 4)
        img_gray = convert_img_color(img, ColorFormat.BGR_GRAY)
        self.assertEqual(img_gray.channels, 1)

    def test_draw_rectangles(self):
        img = self.window.grab_mss()
        left_top = Pixel(50, 50)
        right_bottom = Pixel(150, 150)
        rectangles = [Rect(left_top=left_top, right_bottom=right_bottom)]
        draw_rectangles(img, rectangles)
        # Show img
        # show_img(img)

    def test_draw_crosshairs(self):
        img = self.window.grab_mss()
        left_top = Pixel(50, 50)
        right_bottom = Pixel(150, 150)
        rectangles = [Rect(left_top=left_top, right_bottom=right_bottom)]
        draw_crosshairs(img, rectangles)
        # Show img
        # show_img(img)

    def test_draw_circles(self):
        img = self.window.grab_mss()
        left_top = Pixel(50, 50)
        right_bottom = Pixel(150, 150)
        rectangles = [Rect(left_top=left_top, right_bottom=right_bottom)]
        draw_circles(img, rectangles, radius=20)
        # Show img
        # show_img(img)

    def test_draw_lines(self):
        img = self.window.grab_mss()
        left_top = Pixel(50, 50)
        right_bottom = Pixel(150, 150)
        rectangles = [Rect(left_top=left_top, right_bottom=right_bottom)]
        draw_lines(img, rectangles)
        # Show img
        # show_img(img)
