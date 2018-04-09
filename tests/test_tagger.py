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


if __name__ == '__main__':
    unittest.main()
