import os
from unittest import TestCase, skip

import cv2 as cv
import numpy as np

from config import settings
from core.display.window import WindowHandler

from ..entities import (
    Color,
    Img,
    ImgBase,
    ImgLoader,
    Pixel,
    Polygon,
    Rect,
    SearchResult,
)
from ..enums import ColorFormat


class PixelTests(TestCase):
    def test_attributes(self):
        x = 10.5
        y = 20.5
        loc = Pixel(x=x, y=y)

        self.assertEqual(loc.x, x)
        self.assertEqual(loc.y, y)

    def test_iteration(self):
        x = 10.5
        y = 20.5
        loc = Pixel(x=x, y=y)

        coordinates = list(loc)
        self.assertEqual(coordinates, [x, y])

    def test_immutable(self):
        loc = Pixel(x=10.5, y=20.5)

        with self.assertRaises(AttributeError):
            loc.x = 30.5

    def test_equality(self):
        loc1 = Pixel(x=10.5, y=20.5)
        loc2 = Pixel(x=10.5, y=20.5)
        loc3 = Pixel(x=30.5, y=40.5)

        self.assertEqual(loc1, loc2)
        self.assertNotEqual(loc1, loc3)


class RectTests(TestCase):
    def setUp(self) -> None:
        self.left_top = Pixel(x=10.5, y=20.5)
        self.right_bottom = Pixel(x=30.5, y=40.5)
        self.width = 20
        self.height = 20

    def test_post_init_attributes_validation(self):
        err_msg = "Either right_bottom or both width and height must be provided."

        test_cases = [
            {"left_top": self.left_top},
            {"left_top": self.left_top, "width": self.width},
            {"left_top": self.left_top, "height": self.height},
        ]

        for kwargs in test_cases:
            with self.assertRaisesRegex(ValueError, err_msg):
                Rect(**kwargs)

    def test_attributes(self):
        width = self.right_bottom.x - self.left_top.x
        height = self.right_bottom.y - self.left_top.y
        expected_center_x = round((self.left_top.x + self.right_bottom.x) / 2)
        expected_center_y = round((self.left_top.y + self.right_bottom.y) / 2)

        test_cases = [
            {"left_top": self.left_top, "right_bottom": self.right_bottom},
            {"left_top": self.left_top, "width": self.width, "height": self.height},
        ]

        for kwargs in test_cases:
            rect = Rect(**kwargs)
            self.assertEqual(rect.left_top, self.left_top)
            self.assertEqual(rect.right_bottom, self.right_bottom)
            self.assertEqual(rect.width, width)
            self.assertEqual(rect.height, height)
            self.assertEqual(rect.center.x, expected_center_x)
            self.assertEqual(rect.center.y, expected_center_y)

    def test_iteration(self):
        rect = Rect(left_top=self.left_top, right_bottom=self.right_bottom)
        rect_values = list(rect)
        expected_values = [self.left_top, self.right_bottom, self.width, self.height]
        self.assertEqual(rect_values, expected_values)


class PolygonTests(TestCase):
    def test_valid_polygon(self):
        points = [
            Pixel(x=0, y=0),
            Pixel(x=0, y=1),
            Pixel(x=1, y=1),
            Pixel(x=1, y=0),
        ]
        polygon = Polygon(points)
        self.assertEqual(polygon.points, points)

    def test_invalid_polygon(self):
        points = [
            Pixel(x=0, y=0),
            Pixel(x=0, y=1),
            Pixel(x=1, y=1),
        ]
        with self.assertRaises(ValueError):
            Polygon(points)

    def test_as_np_array(self):
        points = [
            Pixel(x=0, y=0),
            Pixel(x=0, y=1),
            Pixel(x=1, y=1),
            Pixel(x=1, y=0),
        ]
        polygon = Polygon(points)
        expected_np_array = np.array([(0, 0), (0, 1), (1, 1), (1, 0)])
        np.testing.assert_array_equal(polygon.as_np_array(), expected_np_array)


class ImgBaseTests(TestCase):
    def setUp(self) -> None:
        self.img_path = "static/tests/vision/test_template.png"
        self.loaded_img = cv.imread(self.img_path)
        self.height, self.width, self.channels = self.loaded_img.shape
        self.img = ImgBase()
        self._set_img_attributes()

    def _set_img_attributes(self):
        self.img._data = self.loaded_img
        self.img._set_params()

    def test_attributes(self):
        self.assertTrue(np.array_equal(self.img.initial, self.loaded_img))
        self.assertTrue(np.array_equal(self.img.initial, self.img.data))
        self.assertFalse(self.img.path)
        self.assertFalse(self.img.confidence)
        self.assertEqual(self.img.width, self.width)
        self.assertEqual(self.img.height, self.height)
        self.assertEqual(self.img.channels, self.channels)

    def test_iter(self):
        expected_lst = (self.width, self.height, self.channels)
        img_lst = tuple(self.img)
        self.assertEqual(img_lst, expected_lst)

    def test_reset(self):
        new_data = "123"
        self.img.data = new_data
        self.assertEqual(self.img.data, new_data)
        self.img.reset()
        self.assertTrue(np.array_equal(self.img.initial, self.img.data))

    def test_save(self):
        new_img_path = "tests/test_save.png"
        self.img.save(new_img_path)
        # Test image was saved
        img = cv.imread(settings.STATIC_PATH + new_img_path)
        height, width, channels = img.shape
        self.assertEqual(width, self.width)
        self.assertEqual(height, self.height)
        self.assertEqual(channels, self.channels)
        # Delete the test image
        os.remove(settings.STATIC_PATH + new_img_path)

    def test_crop(self):
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
            self.img.crop(case["rect"])
            self.assertEqual(self.img.width, width)
            self.assertEqual(self.img.height, height)
            self.img.reset()

    def test_crop_polygon(self):
        window = WindowHandler()
        img = window.grab()
        region = Polygon(
            [Pixel(100, 500), Pixel(500, 250), Pixel(1000, 600), Pixel(500, 800)]
        )
        width, height = 900, 550
        img.crop_polygon(region)
        # Test image was cropped
        self.assertEqual(img.width, width)
        self.assertEqual(img.height, height)
        # Test pixel color at (10, 10)
        pixel_color = img.data[10, 10]
        expected_color = (0, 0, 0)
        for channel_value, expected_value in zip(pixel_color, expected_color):
            self.assertEqual(channel_value, expected_value)

    def test_resize_up(self):
        size = Pixel(1000, 1500)
        self.img.resize(size)
        self.assertEqual(self.img.width, size.x)
        self.assertEqual(self.img.height, size.y)

    def test_resize_down(self):
        size = Pixel(100, 150)
        self.img.resize(size)
        self.assertEqual(self.img.width, size.x)
        self.assertEqual(self.img.height, size.y)

    def test_resize_x_up(self):
        self.img.resize_x(2)
        self.assertEqual(self.img.width, self.width * 2)
        self.assertEqual(self.img.height, self.height * 2)

    def test_resize_x_down(self):
        self.img.resize_x(0.5)
        self.assertAlmostEqual(self.img.width, self.width / 2, delta=0.5)
        self.assertAlmostEqual(self.img.height, self.height / 2, delta=0.5)

    def test_cvt_color(self):
        self.assertEqual(self.img.channels, 3)
        # convert gray
        self.img.cvt_color(ColorFormat.BGR_GRAY)
        self.assertEqual(self.img.channels, 1)
        # convert bgr
        self.img.cvt_color(ColorFormat.BGR)
        self.assertEqual(self.img.channels, 3)
        # convert bgr-rgb
        self.img.cvt_color(ColorFormat.BGR_RGB)
        self.assertEqual(self.img.channels, 3)

    @skip("Popup window")
    def test_show(self):
        self.img.show(window_name="Test window")


class ImgTests(TestCase):
    def setUp(self) -> None:
        self.img_path = "static/tests/vision/test_template.png"
        self.loaded_img = cv.imread(self.img_path)
        self.height, self.width, self.channels = self.loaded_img.shape
        self.img = Img(self.loaded_img)

    def test_init_attributes(self):
        self.assertTrue(np.array_equal(self.img.initial, self.loaded_img))
        self.assertTrue(np.array_equal(self.img.initial, self.img.data))
        self.assertFalse(self.img.path)
        self.assertFalse(self.img.confidence)
        self.assertEqual(self.img.width, self.width)
        self.assertEqual(self.img.height, self.height)
        self.assertEqual(self.img.channels, self.channels)


class ImgLoaderTests(TestCase):
    def setUp(self) -> None:
        self.img_path = "tests/vision/test_template.png"
        self.loaded_img = cv.imread(settings.STATIC_PATH + self.img_path)
        self.height, self.width, self.channels = self.loaded_img.shape

    def test_loader(self):
        img = ImgLoader(self.img_path, 0.8, ColorFormat.GRAY)
        self.assertFalse(np.array_equal(img.initial, self.loaded_img))
        self.assertTrue(np.array_equal(img.initial, img.data))
        self.assertEqual(img.path, self.img_path)
        self.assertEqual(img.confidence, 0.8)
        self.assertEqual(img.width, self.width)
        self.assertEqual(img.height, self.height)
        self.assertEqual(img.channels, 1)

    def test_loader_not_found(self):
        with self.assertRaises(FileNotFoundError):
            ImgLoader("not_found.png", 0.8, ColorFormat.GRAY)


class ColorTests(TestCase):
    def test_color_creation_valid_rgb(self):
        # Test creating Color object with valid RGB values
        color = Color(r=255, g=128, b=64)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 128)
        self.assertEqual(color.b, 64)
        self.assertIsNone(color.a)

    def test_color_creation_valid_rgba(self):
        # Test creating Color object with valid RGBA values
        color = Color(r=255, g=128, b=64, a=200)
        self.assertEqual(color.r, 255)
        self.assertEqual(color.g, 128)
        self.assertEqual(color.b, 64)
        self.assertEqual(color.a, 200)

    def test_color_creation_invalid_rgb(self):
        # Test creating Color object with invalid RGB values
        with self.assertRaises(ValueError):
            Color(r=-1, g=128, b=64)

        with self.assertRaises(ValueError):
            Color(r=255, g=300, b=64)

        with self.assertRaises(ValueError):
            Color(r=255, g=128, b=-10)

    def test_color_creation_invalid_rgba(self):
        # Test creating Color object with invalid RGBA values
        with self.assertRaises(ValueError):
            Color(r=255, g=128, b=64, a=-1)

        with self.assertRaises(ValueError):
            Color(r=255, g=128, b=64, a=300)

    def test_from_rgb(self):
        # Test creating Color object from RGB values
        rgb = (100, 150, 200)
        color = Color.from_rgb(rgb)
        self.assertEqual(color.r, 100)
        self.assertEqual(color.g, 150)
        self.assertEqual(color.b, 200)
        self.assertIsNone(color.a)

    def test_from_rgb_invalid(self):
        err_msg = "Invalid RGB values. Expected a tuple of length 3 or 4."
        with self.assertRaisesRegex(ValueError, err_msg):
            Color.from_rgb((200, 150, 100, 0, 0))

    def test_from_bgr(self):
        # Test creating Color object from BGR values
        bgr = (200, 150, 100)
        color = Color.from_bgr(bgr)
        self.assertEqual(color.r, 100)
        self.assertEqual(color.g, 150)
        self.assertEqual(color.b, 200)
        self.assertIsNone(color.a)

    def test_from_bgr_invalid(self):
        err_msg = "Invalid BGR values. Expected a tuple of length 3 or 4."
        with self.assertRaisesRegex(ValueError, err_msg):
            Color.from_bgr((200, 150, 100, 0, 0))

    def test_to_rgb(self):
        # Test converting Color object to RGB values
        color = Color(r=100, g=150, b=200, a=50)
        rgb = color.to_rgb()
        self.assertEqual(rgb, (100, 150, 200, 50))

        color = Color(r=100, g=150, b=200)
        rgb = color.to_rgb()
        self.assertEqual(rgb, (100, 150, 200))

    def test_to_bgr(self):
        # Test converting Color object to BGR values
        color = Color(r=100, g=150, b=200, a=50)
        bgr = color.to_bgr()
        self.assertEqual(bgr, (200, 150, 100, 50))

        color = Color(r=100, g=150, b=200)
        bgr = color.to_bgr()
        self.assertEqual(bgr, (200, 150, 100))


class SearchResultTests(TestCase):
    def setUp(self):
        self.ref_img = Img(data=np.zeros((10, 10), dtype=np.uint8))
        self.search_img = Img(data=np.zeros((20, 20), dtype=np.uint8))
        self.confidence = 0.8
        self.rect1 = Rect(left_top=Pixel(x=5, y=5), right_bottom=Pixel(x=15, y=15))
        self.rect2 = Rect(left_top=Pixel(x=10, y=10), right_bottom=Pixel(x=20, y=20))
        self.search_result = SearchResult(
            ref_img=self.ref_img, search_img=self.search_img
        )

    def test_len(self):
        self.assertEqual(len(self.search_result), 0)
        self.search_result.add(self.rect1)
        self.assertEqual(len(self.search_result), 1)

    def test_iter(self):
        self.search_result.add(self.rect1)
        self.search_result.add(self.rect2)
        r1, r2 = self.search_result
        self.assertEqual(r1, self.rect1)
        self.assertEqual(r2, self.rect2)

    def test_bool(self):
        self.assertFalse(self.search_result)
        self.search_result.add(self.rect1)
        self.assertTrue(self.search_result)

    def test_repr(self):
        self.search_result.add(self.rect1)
        self.search_result.add(self.rect2)
        self.assertEqual(
            repr(self.search_result),
            f"<SearchResult(count={self.search_result.count}, locations=[{self.rect1}, {self.rect2}])>",
        )

    def test_attributes(self):
        self.assertEqual(self.search_result.ref_img, self.ref_img)
        self.assertEqual(self.search_result.search_img, self.search_img)
        self.assertEqual(self.search_result.locations, [])
        self.assertEqual(self.search_result.count, 0)

    def test_add(self):
        self.search_result.add(self.rect1)
        self.assertEqual(len(self.search_result), 1)
        self.assertEqual(self.search_result.locations, [self.rect1])

        self.search_result.add(self.rect2)
        self.assertEqual(len(self.search_result), 2)
        self.assertEqual(self.search_result.locations, [self.rect1, self.rect2])

    def test_remove(self):
        self.search_result.add(self.rect1)
        self.assertEqual(len(self.search_result), 1)
        self.search_result.remove(self.rect1)
        self.assertEqual(len(self.search_result), 0)
