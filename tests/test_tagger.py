"""
    tests.tagger
    ~~~~~~~~~~~~~
"""
import unittest
import mock
from llamedl.tagger import Tagger


class DummyEasyID3():
    audio = None

    def __init__(self, *args, **kw):
        pass

    def get(self, k, d=None):
        return self.audio

    def update(self, d):
        pass

    def save(self, v1=None):
        pass


class TestTagger(unittest.TestCase):
    def setUp(self):
        self.t = Tagger()
        self.tags_list = ['foo', 'bar', 'foobar']

        info_mock = mock.patch('llamedl.tagger.EasyID3', new=DummyEasyID3)
        self.info_patch = info_mock.start()

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

    def test_filter_tags__whitelist(self):
        self.t.whitelist = ['foo']
        self.t.blacklist = None
        result = self.t.filter_tags(self.tags_list)
        self.assertListEqual(['foo'], result)

    @mock.patch("llamedl.tagger.Tagger.get_tags", return_value=["gen", "re"])
    @mock.patch("llamedl.tagger.EasyID3.update")
    def test_add_tags_to_file__tags_exist(self, update_patch, tags_patch):
        self.info_patch.audio = ['foo', 'bar']
        self.t.add_tags_to_file("foobar - barfoo", '/foo/bar')
        update_patch.assert_not_called()

    @mock.patch("llamedl.tagger.Tagger.get_tags", return_value=["gen", "re"])
    @mock.patch("llamedl.tagger.EasyID3.update")
    def test_add_tags_to_file__tags_doesnt_exist(self, update_patch, tags_patch):
        self.info_patch.audio = False
        self.t.add_tags_to_file("foobar - barfoo", '/foo/bar')
        tags_patch.assert_called_with("Foobar")
        update_patch.assert_called_with({'albumartist': 'VA', 'album': '2018',
                                         'title': 'Barfoo', 'copyright': 'LlameDL',
                                         'artist': 'Foobar', 'date': '2018', 'genre': 'gen\\re'})


if __name__ == '__main__':
    unittest.main()
