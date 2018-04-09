import unittest
from llamedl.utill import remove_descriptions, change_string_to_tags, capitalize_first_char, create_filename


class Test(unittest.TestCase):
    def test__remove_descriptions__output_this_same(self):
        result = remove_descriptions("foobar")
        self.assertEqual("foobar", result)

    def test__remove_descriptions__good_output(self):
        result = remove_descriptions("foobar [Official Music]")
        self.assertEqual("foobar", result)

    def test__remove_descriptions__two_tags_to_remove(self):
        result = remove_descriptions("foobar [Official Music][HD]")
        self.assertEqual("foobar", result)

    def test__change_string_to_tags__artist_and_title(self):
        result = change_string_to_tags("foo - bar")
        self.assertDictEqual({'artist': 'Foo', 'title': 'Bar'}, result)

    def test__change_string_to_tags__only_title(self):
        result = change_string_to_tags("foobar")
        self.assertDictEqual({'artist': 'Unknown', 'title': 'Foobar'}, result)

    def test__capitalize_first_char__first_char_low(self):
        result = capitalize_first_char("fooBar")
        self.assertEqual("FooBar", result)

    def test__capitalize_first_char__first_char_up(self):
        result = capitalize_first_char("FooBar")
        self.assertEqual("FooBar", result)

    def test__create_filename__good_output(self):
        result = create_filename("Foo - Bar")
        self.assertEqual("Foo - Bar", result)

    def test__create_filename__tags_to_remove(self):
        result = create_filename("Foo - Bar[HD]")
        self.assertEqual("Foo - Bar", result)

    def test__create_filename__small_letters(self):
        result = create_filename("foo - bar")
        self.assertEqual("Foo - Bar", result)


if __name__ == '__main__':
    unittest.main()
