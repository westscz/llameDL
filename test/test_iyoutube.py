import unittest
import mock
from llamedl.iyoutube import IYouTube


class TestIYouTube(unittest.TestCase):
    def setUp(self):
        self.iyt = IYouTube("")
        info_mock = mock.patch('llamedl.iyoutube.IYouTube.url_info', new_callable=mock.PropertyMock)
        self.info_patch = info_mock.start()

    def test__get_title__unknown_artist(self):
        self.info_patch.return_value = {'title': 'Foobar'}
        ret = self.iyt.get_title()
        self.assertEqual(ret, 'Unknown - Foobar')

    def test__get_title__known_artist(self):
        self.info_patch.return_value = {'title': 'Foo - Bar'}
        ret = self.iyt.get_title()
        self.assertEqual(ret, 'Foo - Bar')

    def test__get_title__necessary_description(self):
        self.info_patch.return_value = {'title': 'Foo - Bar (video music)'}
        ret = self.iyt.get_title()
        self.assertEqual(ret, 'Foo - Bar')

    def test__is_playlist__true(self):
        self.info_patch.return_value = {'_type': 'Playlist'}
        self.assertTrue(self.iyt.is_playlist())

    def test__is_playlist__false(self):
        self.info_patch.return_value = {'_type': None}
        self.assertFalse(self.iyt.is_playlist())


if __name__ == '__main__':
    unittest.main()
