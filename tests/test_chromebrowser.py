"""
    tests.ichrome
    ~~~~~~~~~~~~~
"""
import unittest

import mock
from llamedl.browser.chromebrowser import ChromeBrowser


class TestChromeBrowser(unittest.TestCase):
    def setUp(self):
        bookmarks_mock = mock.patch("llamedl.browser.chromebrowser.ChromeBrowser.bookmarks",
                                    new_callable=mock.PropertyMock)
        self.bookmarks_patch = bookmarks_mock.start()
        self.ich = ChromeBrowser()

    def test_get_folder__exist(self):
        expected_result = [{}]
        self.bookmarks_patch.return_value = [{'type': 'folder',
                                              'name': 'foobar', 'children': expected_result}]
        result = self.ich.get_folder("foobar")
        self.assertListEqual(expected_result, result)

    def test_get_folder__not_exist(self):
        expected_result = []
        self.bookmarks_patch.return_value = [{'type': 'folder',
                                              'name': 'foobar', 'children': expected_result}]
        with self.assertRaises(IndexError):
            result = self.ich.get_folder("foo")
            self.assertListEqual(expected_result, result)

    @mock.patch("llamedl.browser.chromebrowser.ChromeBrowser.get_folder")
    def test_get_yt_urls__exist(self, folder_mock):
        url = "youtube.com/foo/bar"
        expected_result = [url]
        folder_mock.return_value = [{'url': url}]
        result = self.ich.get_youtube_urls_from_folder("foobar")
        self.assertListEqual(expected_result, result)

    @mock.patch("llamedl.browser.chromebrowser.ChromeBrowser.get_folder")
    def test_get_yt_urls__not_exist(self, folder_mock):
        url = "vimeo.com/foo/bar"
        folder_mock.return_value = [{'url': url}]
        expected = []
        result = self.ich.get_youtube_urls_from_folder("foo")
        self.assertListEqual(expected, result)
