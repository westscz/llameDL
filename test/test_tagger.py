import unittest
import mock
from llamedl.tagger import Tagger


class TestTagger(unittest.TestCase):
    def setUp(self):
        self.t = Tagger()

    # requests mock
    # def test__get_tags_from_last_fm(self, get_patch):
    #     get_patch.return_value = {}
    #     self.t.get_tags_from_last_fm('foo')

    @mock.patch("musicbrainzngs.search_artists")
    def test__get_tags_from_musicbrainzgs__match(self, search_artist_patch):
        expected_result = ['bar']
        search_artist_patch.return_value = {'artist-count': 1,
                                            'artist-list': [{'name': 'foo', 'tag-list': expected_result}]}
        result = self.t.get_tags_from_musicbrainzgs('foo')
        self.assertListEqual(expected_result, result)

    @mock.patch("musicbrainzngs.search_artists")
    def test__get_tags_from_musicbrainzgs__empty(self, search_artist_patch):
        search_artist_patch.return_value = {'artist-count': 0}
        result = self.t.get_tags_from_musicbrainzgs('foo')
        self.assertListEqual([], result)


if __name__ == '__main__':
    unittest.main()
