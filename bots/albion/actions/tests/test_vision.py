from unittest import TestCase

from core.common.entities import ImgLoader

from ..vision import AlbionVision


class AlbionVisionTests(TestCase):
    def setUp(self) -> None:
        self.vision = AlbionVision()
        self.cases = {
            "pass": [
                ImgLoader("albion/tests/1.png"),
                ImgLoader("albion/tests/2.png"),
                ImgLoader("albion/tests/9.png"),
                ImgLoader("albion/tests/11.png"),
            ],
            "casting": [
                ImgLoader("albion/tests/12.png"),
                ImgLoader("albion/tests/13.png"),
                ImgLoader("albion/tests/17.png"),
                ImgLoader("albion/tests/18.png"),
            ],
            "mounted": [
                ImgLoader("albion/tests/5.png"),
                ImgLoader("albion/tests/6.png"),
                # ImgLoader("albion/tests/12.png"),  # teleport on cooldown
            ],
            "gathering_failed": [
                ImgLoader("albion/tests/14.png"),
                ImgLoader("albion/tests/16.png"),
            ],
            "gathering_done": [ImgLoader("albion/tests/15.png")],
        }

    def test_is_mounting(self):
        for i, case in enumerate(self.cases["casting"]):
            self.assertTrue(self.vision.is_mounting(case), f"Failed: {i}")
        for i, case in enumerate(self.cases["pass"]):
            self.assertFalse(self.vision.is_mounting(case), f"Failed: {i}")

    def test_is_mounted(self):
        for i, case in enumerate(self.cases["mounted"]):
            self.assertTrue(self.vision.is_mounted(case), f"Failed: {i}")
        for i, case in enumerate(self.cases["pass"]):
            self.assertFalse(self.vision.is_mounted(case), f"Failed: {i}")

    def test_is_gathering(self):
        for i, case in enumerate(self.cases["casting"]):
            self.assertTrue(self.vision.is_gathering(case), f"Failed: {i}")
        for i, case in enumerate(self.cases["pass"]):
            self.assertFalse(self.vision.is_gathering(case), f"Failed: {i}")

    def test_is_gathering_failed(self):
        for i, case in enumerate(self.cases["gathering_failed"]):
            self.assertTrue(self.vision.is_gathering_failed(case), f"Failed: {i}")

    def test_is_gathering_done(self):
        for i, case in enumerate(self.cases["gathering_done"]):
            self.assertTrue(self.vision.is_gathering_done(case), f"Failed: {i}")
