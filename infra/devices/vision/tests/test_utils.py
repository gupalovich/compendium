import os
from unittest import TestCase, skip

from config import settings
from infra.common.entities import Img
from infra.devices.vision.enums import ColorFormat

from ..utils import crop_img, load_img, resize_img, save_img, show_img


class UtilsTests(TestCase):
    def setUp(self) -> None:
        self.static_path = settings.STATIC_PATH
        self.img_path = "tests/test_template.png"
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
        pass
