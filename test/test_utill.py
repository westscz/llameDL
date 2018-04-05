import unittest
from common.utill import remove_descriptions, change_string_to_tags


class Test(unittest.TestCase):
    def test__remove_descriptions__output_this_same(self):
        result = remove_descriptions("foobar")
        self.assertEqual("foobar", result)

    def test__remove_descriptions__good_output(self):
        result = remove_descriptions("foobar [Official Music]")
        self.assertEqual("foobar", result)

    def test__change_string_to_tags__artist_and_title(self):
        result = change_string_to_tags("foo - bar")
        self.assertDictEqual({'artist': 'foo', 'title': 'bar'}, result)

    def test__change_string_to_tags__only_title(self):
        result = change_string_to_tags("foobar")
        self.assertDictEqual({'artist': 'Unknown', 'title': 'foobar'}, result)


if __name__ == '__main__':
    unittest.main()
