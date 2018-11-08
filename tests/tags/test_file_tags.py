import unittest
from llamedl.tags.filetags import FileTags


class TestFileTags(unittest.TestCase):
    def setUp(self):
        self.obj = FileTags("/foo/bar")
        self.obj._file_content = {'foo': ['Dance', 'Pop']}

    def test_get_tags__available(self):
        result = self.obj.get_tags('foo')
        self.assertEqual(['Dance', 'Pop'], result)

    def test_get_tags__not_available(self):
        result = self.obj.get_tags('bar')
        self.assertEqual([], result)
