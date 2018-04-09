"""
    tests.tagger
    ~~~~~~~~~~~~~
"""
import unittest
import mock
from llamedl.tagger import Tagger


class TestTagger(unittest.TestCase):
    def setUp(self):
        self.t = Tagger()
        self.tags_list = ['foo','bar', 'foobar']

    @mock.patch("musicbrainzngs.search_artists")
    def test_get_tags_from_musicbrainzgs__match(self, search_artist_patch):
        expected_result = ['Bar']
        search_artist_patch.return_value = {'artist-count': 1,
                                            'artist-list':
                                                [{'name': 'foo', 'tag-list': [{'name': 'bar'}]}]}
        result = self.t.get_tags_from_musicbrainzgs('foo')
        self.assertListEqual(expected_result, result)

    @mock.patch("musicbrainzngs.search_artists")
    def test_get_tags_from_musicbrainzgs__empty(self, search_artist_patch):
        search_artist_patch.return_value = {'artist-count': 0}
        result = self.t.get_tags_from_musicbrainzgs('foo')
        self.assertListEqual([], result)

    def test_filter_tags_with_whitelist(self):
        self.t.whitelist = ['foo']
        result = self.t.filter_tags_with_whitelist(self.tags_list)
        self.assertListEqual(['foo'], result)

    def test_filter_tags_with_blacklist(self):
        self.t.blacklist = ['bar']
        result = self.t.filter_tags_with_blacklist(self.tags_list)
        self.assertListEqual(['foo', 'foobar'], result)

    def test_filter_tags__whitelist(self):
        self.t.whitelist = ['foo']
        self.t.blacklist = None
        result = self.t.filter_tags(self.tags_list)
        self.assertListEqual(['foo'], result)

    def test_filter_tags__blacklist(self):
        self.t.whitelist = None
        self.t.blacklist = ['bar']
        result = self.t.filter_tags(self.tags_list)
        self.assertListEqual(['foo', 'foobar'], result)

    def test_filter_tags__all(self):
        self.t.whitelist = ['foo', 'foobar']
        self.t.blacklist = ['foo']
        result = self.t.filter_tags(self.tags_list)
        self.assertListEqual(['foobar'], result)


if __name__ == '__main__':
    unittest.main()
