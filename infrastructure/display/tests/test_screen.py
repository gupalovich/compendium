from unittest import TestCase

import numpy as np

from ..screen import Screen


class TestScreen(TestCase):
    def setUp(self) -> None:
        pass

    def test_grab_without_process(self):
        result = Screen.grab()
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape[2], 3)
        self.assertGreater(result.shape[0], 0)
        self.assertGreater(result.shape[1], 0)
