import unittest

from llamedl.tagsproviders.filetags import FileTags
from tests.utils import create_tags_file


class TestFileTags(unittest.TestCase):
    def setUp(self):
        self.data = {"Infected Mushroom": ["Electronic", "Dubstep"]}
        filepath = create_tags_file(self.data)
        self.obj = FileTags(filepath)

    def test_get_tags__available(self):
        expected = ["Electronic", "Dubstep"]
        result = self.obj.get_tags("Infected Mushroom")

        self.assertEqual(expected, result)

    def test_get_tags__not_available(self):
        expected = []
        result = self.obj.get_tags("Deadmau5")

        self.assertEqual(expected, result)

    def test_get_tags__no_file(self):
        obj = FileTags("")
        expected = []
        result = obj.get_tags("Infected Mushroom")

        self.assertEqual(expected, result)
