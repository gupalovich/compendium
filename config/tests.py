from unittest import TestCase

from config import settings


class TestConfig(TestCase):
    def setUp(self) -> None:
        pass

    def test_constants(self):
        self.assertTrue(settings.DEFAULT)
        self.assertIsInstance(settings.DEBUG, bool)
        self.assertIsInstance(settings.STATIC_PATH, str)
        self.assertTrue(settings.STATIC_PATH.endswith("/"))
