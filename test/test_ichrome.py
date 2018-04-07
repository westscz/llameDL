import unittest
import mock
from llamedl.ichrome import IChrome


class TestIChrome(unittest.TestCase):
    def setUp(self):
        bookmarks_mock = mock.patch("llamedl.ichrome.IChrome.bookmarks", new_callable=mock.PropertyMock)
        self.bookmarks_patch = bookmarks_mock.start()
        self.ich = IChrome()

    def test__get_folder__exist(self):
        expected_result = [{}]
        self.bookmarks_patch.return_value = [{'type': 'folder', 'name': 'foobar', 'children': expected_result}]
        result = self.ich.get_folder("foobar")
        self.assertListEqual(expected_result, result)

    def test__get_folder__not_exist(self):
        expected_result = []
        self.bookmarks_patch.return_value = [{'type': 'folder', 'name': 'foobar', 'children': expected_result}]
        result = self.ich.get_folder("foo")
        self.assertListEqual(expected_result, result)

    @mock.patch("llamedl.ichrome.IChrome.get_folder")
    def test__get_yt_urls__exist(self, folder_mock):
        url = "youtube.com/foo/bar"
        expected_result = [url]
        folder_mock.return_value = [{'url': url}]
        result = self.ich.get_yt_urls("foobar")
        self.assertListEqual(expected_result, result)

    @mock.patch("llamedl.ichrome.IChrome.get_folder")
    def test__get_yt_urls__not_exist(self, folder_mock):
        url = "vimeo.com/foo/bar"
        expected_result = []
        folder_mock.return_value = [{'url': url}]
        result = self.ich.get_yt_urls("foo")
        self.assertListEqual(expected_result, result)