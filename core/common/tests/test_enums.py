from unittest import TestCase

from ..enums import State


class StateTests(TestCase):
    def setUp(self) -> None:
        self.state_len = 6

    def test_attribute_length(self):
        self.assertEqual(len(State), self.state_len)

    def test_attribute_names(self):
        self.assertEqual(State.INITIAL.name, "INITIAL")
        self.assertEqual(State.STARTED.name, "STARTED")
        self.assertEqual(State.STOPPED.name, "STOPPED")
        self.assertEqual(State.MOVING.name, "MOVING")
        self.assertEqual(State.GATHERING.name, "GATHERING")
        self.assertEqual(State.SEARCHING.name, "SEARCHING")

    def test_attribute_values(self):
        self.assertEqual(State.INITIAL.value, 0)
        self.assertIsInstance(State.STARTED.value, int)
        self.assertIsInstance(State.STOPPED.value, int)
        self.assertIsInstance(State.MOVING.value, int)
        self.assertIsInstance(State.GATHERING.value, int)
        self.assertIsInstance(State.SEARCHING.value, int)
