"""
    tests.iyoutube
    ~~~~~~~~~~~~~
"""
import unittest

import mock
from llamedl.downloaders.youtubedownloader import YouTubeDownloader


class TestIYouTube(unittest.TestCase):
    def setUp(self):
        self.iyt = YouTubeDownloader('')
        info_mock = mock.patch('llamedl.iyoutube.IYouTube.url_info', new_callable=mock.PropertyMock)
        self.info_patch = info_mock.start()

    def test_get_title__unknown_artist(self):
        self.info_patch.return_value = {'title': 'Foobar'}
        result = self.iyt.get_title()
        self.assertEqual(result, 'Unknown - Foobar')

    def test_get_title__known_artist(self):
        self.info_patch.return_value = {'title': 'Foo - Bar'}
        result = self.iyt.get_title()
        self.assertEqual(result, 'Foo - Bar')

    def test_get_title__necessary_description(self):
        self.info_patch.return_value = {'title': 'Foo - Bar (video music)'}
        result = self.iyt.get_title()
        self.assertEqual(result, 'Foo - Bar')

    def test_is_playlist__true(self):
        self.info_patch.return_value = {'_type': 'Playlist'}
        self.assertTrue(self.iyt.is_playlist())

    def test_is_playlist__false(self):
        self.info_patch.return_value = {'_type': None}
        self.assertFalse(self.iyt.is_playlist())

    def test_get_playlist__empty(self):
        self.info_patch.return_value = {'title': 'Foobar'}
        result = self.iyt.get_playlist()
        self.assertListEqual([], result)

    def test_get_playlist__entries_exist(self):
        webpage_url = 'foo.bar'
        self.info_patch.return_value = {'entries': [{'webpage_url': webpage_url}]}
        result = self.iyt.get_playlist()
        self.assertListEqual([webpage_url], result)

    def test_verify_url__is_playlist(self):
        webpage_url = 'foo.bar'
        expected_result = '{}/1'.format(webpage_url)
        self.info_patch.return_value = {'_type': 'Playlist', 'entries': [{'webpage_url': expected_result}]}
        result = self.iyt.verify_url(webpage_url)
        self.assertListEqual(result, [expected_result])

    def test_verify_url__is_not_playlist(self):
        webpage_url = 'foo.bar'
        not_expected_result = '{}/1'.format(webpage_url)
        self.info_patch.return_value = {'webpage_url': not_expected_result}
        result = self.iyt.verify_url(webpage_url)
        self.assertListEqual(result, [webpage_url])


if __name__ == '__main__':
    unittest.main()
